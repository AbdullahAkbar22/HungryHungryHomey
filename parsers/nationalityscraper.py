import requests

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import pyautogui
import time


def getHTMLContent(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
	try:
		with closing(get(url, headers=headers)) as resp:
			return resp.content

	except RequestException as e:
		print('Error during requests to {0} : {1}'.format(url, str(e)))
		return None

def writeNatios():
	ntsource = getHTMLContent('https://www.ef.edu/english-resources/english-grammar/nationalities/')
	if ntsource == None:
		return None
	ntsearch = BeautifulSoup(ntsource, 'html.parser',from_encoding='utf8')
	counter = 1
	nation = ""
	nationality = ""
	outputF = open('nationalities.pl', 'w')
	textline = ""
	onContinents = True
	for result in ntsearch.find_all("td"):
		currenttext = result.text.lower()
		if currenttext == "paris":
			break
		if currenttext == "southeast asian":
			onContinents = False
		currenttext = currenttext.replace(" " , "_")
		print("ctext", currenttext)
		if counter % 3 == 0:
			textline += ").\n"
			outputF.write(textline)
			textline = ""
		elif (counter + 1) % 3 == 0:
			textline += ", " + currenttext
		else:
			if onContinents:
				textline += "continent_to_adjective(" + currenttext
			else:
				textline += "nation_to_nationality(" + currenttext
		counter += 1
	outputF.close()
	
writeNatios()