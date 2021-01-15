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

def getFoodType(foodName):
	foodSource = getHTMLContent('https://www.merriam-webster.com/dictionary/' + foodName)
	if foodSource == None:
		return None
	foodSearch = BeautifulSoup(foodSource, 'html.parser',from_encoding='utf8')
	excludewords = ["a", "this", "the", "that", "is", "specific"]
	possibleFoodTypes = []
	for result in foodSearch.find_all("span", class_="dtText"):
		entry = result.text
		lowerentry = entry.lower()
		print("lower entry is:", lowerentry)
		if "food" in lowerentry:
			splitentry = lowerentry.split("food")
			if len(splitentry) > 1:
				for i in range(len(splitentry) - 1):
					part = splitentry[i].strip()
					partwords = part.split(" ")
					if len(partwords) > 0:
						lastword = partwords[-1]
						if lastword not in excludewords and len(lastword) > 0:
							possibleFoodTypes.append(lastword)
				 
		if "dish" in lowerentry:
			splitentry = lowerentry.split("dish")
			if len(splitentry) > 1:
				for i in range(len(splitentry) - 1):
					part = splitentry[i].strip()
					partwords = part.split(" ")
					if len(partwords) > 0:
						lastword = partwords[-1]
						if lastword not in excludewords and len(lastword) > 0:
							possibleFoodTypes.append(lastword)
							
		return possibleFoodTypes

def type_message(message_text):
	for letteri in range(len(message_text)):
		pyautogui.press(message_text[letteri])
		time.sleep(.2)
	pyautogui.press('enter')
	

print(getFoodType("gyro"))