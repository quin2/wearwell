import json
from flask import Flask, jsonify, Response, request, current_app

import whois
import difflib
import requests

from mechanize import Browser

import pandas as pd
import numpy as np 

import os
import random

def whoisQueryAPI(itemURL):
	kuse = random.choice([current_app.whois_key, current_app.whois_key_2])

	url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
	PARAMS = {'apiKey':kuse, 'domainName': itemURL, 'outputFormat': 'JSON'}
	r = requests.get(url = url, params = PARAMS) 
	data = r.json() 
	if 'dataError' in data['WhoisRecord']:
		return "bad record"
	if 'organization' in data['WhoisRecord']['registrant']:
		return data['WhoisRecord']['registrant']['organization']
	return None

def getBrand(itemURL):
	df = current_app.df

	#check header for brand name first
	br = Browser()
	br.set_handle_robots(False)
	#fake UA so we don't look like a bot
	br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15')]
	br.open(itemURL)
	try2 = br.title()
	br.close()

	matc = [x in try2 for x in df.brand]
	find = np.where(matc)[0]
	if len(find) > 0:
		return df.iloc[find[0]].brand, df.iloc[find[0]].score, None


	#check whois for holding co if we have to (some brands are owned by others)
	org = whoisQueryAPI(itemURL)
	if org is not None:
		if org == "bad record":
			return None, None, "Invalid URL"
		match = difflib.get_close_matches(org, app.df.brand)
		if len(match) >= 1:
			return match[0], df[df.brand == match[0]].score.values[0], None
		matc = [x in org for x in df.brand]
		find = np.where(matc)[0]
		if len(find) > 0:
			return df.iloc[find[0]].brand, df.iloc[find[0]].score, None

	#otherwise we can't find the brand
	return None, None, "Couldn't find brand:("

def getBrand2(itemURL, header):
	df = current_app.df

	try2 = header

	matc = [x in try2 for x in df.brand]
	find = np.where(matc)[0]
	if len(find) > 0:
		return df.iloc[find[0]].brand, df.iloc[find[0]].score, None


	#check whois for holding co if we have to (some brands are owned by others)
	org = whoisQueryAPI(itemURL)
	if org is not None:
		if org == "bad record":
			return None, None, "Invalid URL"
		match = difflib.get_close_matches(org, app.df.brand)
		if len(match) >= 1:
			return match[0], df[df.brand == match[0]].score.values[0], None
		matc = [x in org for x in df.brand]
		find = np.where(matc)[0]
		if len(find) > 0:
			return df.iloc[find[0]].brand, df.iloc[find[0]].score, None

	#otherwise we can't find the brand
	return None, None, "Couldn't find brand:("

def getMaterials(materials):
	df = current_app.mat

	def format(x):
		mats = {}
		mats['material'] = x
		em = df[df['name']==x]['score-emission'].values[0]
		en = df[df['name']==x]['score-energy'].values[0]
		#can change this later...
		mats['sIndex'] = 50 - (em + en)

		return mats
	return [format(x) for x in materials]

app = Flask(__name__)
app.df = pd.read_csv("brandScores.csv")
app.mat = pd.read_csv("fabricScores.csv")
app.whois_key = os.environ.get('WHOISXMLAPI')
app.whois_key_2 = os.environ.get('WHOISXMLAPI2')

@app.route('/')
def index():
	return "made with <3 for wearwell. more info: https://github.com/quin2/wearwell"

@app.route('/v1/brand', methods=['POST'])
def susScore():
	#load from request
	data = request.json
	toScrape = data['url']

	brand, score, err = getBrand(toScrape)

	if err is not None:
		return jsonify (message=err,)

	return jsonify (brand=brand, score=score,)

@app.route('/v2/brand', methods=['POST'])
def susScore2():
	#load from request
	data = request.json
	toScrape = data['url']
	header = data['header']

	brand, score, err = getBrand2(toScrape, header)

	if err is not None:
		return jsonify (message=err,)

	return jsonify (brand=brand, score=score,)

@app.route('/v1/score', methods=['POST'])
def matScore():
	#load from request
	data = request.json
	toScrape = data['url']
	header = data['header']
	material = data['materials']
	material = material[0]

	brand, score, err = getBrand2(toScrape, header)

	data = []

	if material is not None:
		if len(material > 0):
			data = getMaterials(material)

	if err is not None:
		return jsonify (message=err, material=data)

	return jsonify (brand=brand, brandScore=score, material=data)

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True, port=80)
