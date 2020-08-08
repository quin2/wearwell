import json
from flask import Flask, jsonify, Response, request, current_app

import whois
import difflib
import requests

from mechanize import Browser

import pandas as pd
import numpy as np 

apiKey = "at_eFtokGi0dpEWpC2XDyQrbonLLkvFp" #switch to env variables before deploy..

def whoisQueryAPI(itemURL):
	url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
	PARAMS = {'apiKey':apiKey, 'domainName': itemURL, 'outputFormat': 'JSON'}
	r = requests.get(url = url, params = PARAMS) 
	data = r.json() 
	if 'organization' in data['WhoisRecord']['registrant']:
		org = data['WhoisRecord']['registrant']['organization']
	else:
		org = None
	return org

def getBrand(itemURL):
	df = current_app.df
	org = whoisQueryAPI(itemURL)
	if org is not None:
		match = difflib.get_close_matches(org, app.df.brand)
		if len(match) >= 1:
			return match[0], df[df.brand == match[0]].score.values[0], None
		matc = [x in org for x in df.brand]
		find = np.where(matc)[0]
		if len(find) > 0:
			return df.iloc[find[0]].brand, df.iloc[find[0]].score, None


	#check header next...
	br = Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	br.open(itemURL)
	try2 = br.title()
	br.close()

	matc = [x in try2 for x in df.brand]
	find = np.where(matc)[0]
	if len(find) > 0:
		return df.iloc[find[0]].brand, df.iloc[find[0]].score

	return None, None, "Couldn't find brand:("

app = Flask(__name__)
app.df = pd.read_csv("brandScores.csv")

@app.route('/')
def index():
	return "usage: send website URL as {url: 'https://example.com'} to /v1/score and get sustainability info back"

@app.route('/v1/score', methods=['POST'])
def susScore():
	#load from request
	data = request.json
	toScrape = data['url']

	brand, score, err = getBrand(toScrape)

	if err is not None:
		return jsonify (
			message=err,
		)

	return jsonify (
			brand=brand,
			score=score
		)


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True, port=80)
