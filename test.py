import whois
import pandas as pd
import difflib
import requests

from mechanize import Browser

import numpy as np


df = pd.read_csv("brandScores.csv")

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
	
	org = whoisQueryAPI(itemURL)
	if org is not None:
		match = difflib.get_close_matches(org, df.brand)
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



itemURL = "https://us.romwe.com/Guys-Butterfly-Shirt-p-645202-cat-858.html?scici=GuysHomePage~~ON_Banner,CN_catlist0421,HZ_Shirts,HI_hotZonevw54qyki61~~4_3~~real_858~~RPcCccGuysHomepage_default_5182~~~~50001"
lulu = "https://shop.lululemon.com/p/men-shorts/Pace-Breaker-Short-Linerless/_/prod5020227?color=0001&sz=M"
prana = "https://www.prana.com/p/vaha-short/M3VAHS116.html?dwvar_M3VAHS116_color=Russet"


br = getBrand(itemURL)
#print(br)

br = getBrand(lulu)
print(br)

br = getBrand(prana)
print(br)

