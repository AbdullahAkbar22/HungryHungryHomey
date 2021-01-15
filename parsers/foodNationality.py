
import time

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from pyswip import Functor, Variable, Query, call, Prolog

prolog = Prolog()
prolog.consult("nationalities.pl")


def getHTMLContent(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
	
	try:
		with closing(get(url, headers=headers)) as resp:
			return resp.content

	except RequestException as e:
		print('Error during requests to {0} : {1}'.format(url, str(e)))
		return None
		
def bigLetters(passed):
	splitword = passed.split("_")
	finalword = ""
	for i in range(len(splitword)):
		word = splitword[i]
		if len(word) >= 1:
			finalword += word[0].upper() + word[1:]
		if i != len(splitword) - 1:
			finalword += " "
	return finalword
	
def get_food_nation(passed):
	htmlBody = str(getHTMLContent("https://google.com/search?q=" + passed + " food"))
	food_nation = []
	
	if '"wp-tabs-container"' not in htmlBody:
		return None
	foodSearch = BeautifulSoup(htmlBody, 'html.parser')
	secondFoodSearch = BeautifulSoup(foodSearch.find(id="wp-tabs-container").encode_contents(), 'html.parser')
	for result in foodSearch.find_all("div", class_="rVusze"):
		lowertext = result.text.lower()
		if "origin" in lowertext:
			splittext = lowertext.split(": ")
			if len(splittext) > 1:
				nationsOfOrigin = splittext[-1].split(",")
				for nation in nationsOfOrigin:
					nation = nation.strip()
					nation = nation.replace(" ", "_")
					food_nation.append(nation)
				return food_nation
			 
	return None

def get_food_type(passed):
	htmlBody = str(getHTMLContent("https://google.com/search?q=" + passed + " food"))
	
	if '"wp-tabs-container"' not in htmlBody:
		return None
	foodSearch = BeautifulSoup(htmlBody, 'html.parser')
	for result in foodSearch.find_all("div", class_="wwUB2c"):
		lowertext = result.text.lower()
		return lowertext
	return None
	
def get_food_nationality(passed):
	if passed == None:
		return None
	food_nationalities = []
	for keyword in passed:
		for result in list(prolog.query("nation_to_nationality("+keyword+", NATIONALITY); continent_to_adjective("+keyword+", NATIONALITY).")):
			food_nationalities.append(result["NATIONALITY"])
	
	return food_nationalities
	
theInp = input("enter a food: ")
print(get_food_type(theInp))
foodnatarr = get_food_nationality(get_food_nation(theInp))

print(foodnatarr)

suggestion_arr = []
for item in foodnatarr:
	counter = 0
