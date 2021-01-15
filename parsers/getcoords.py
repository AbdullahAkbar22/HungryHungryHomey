import time

from requests import get
from requests.exceptions import RequestException
from contextlib import closing

def getHTMLContent(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
	try:
		with closing(get(url, headers=headers)) as resp:
			return resp.content

	except RequestException as e:
		print('Error during requests to {0} : {1}'.format(url, str(e)))
		return None
		

	

def get_coords(locationPassed):
	locationPassed = sanitize(locationPassed)
	locationPassed = locationPassed.replace(" " , "+")
	#mapContent = str(getHTMLContent("https://www.google.com/maps/place/" + locationPassed))
	mapContent = str(getHTMLContent("https://www.google.com/maps/search/?api=1&query=" + locationPassed))
	
	if "window.APP_INITIALIZATION_STATE=[[[" not in mapContent:
		return None
	coords = mapContent.split("window.APP_INITIALIZATION_STATE=[[[")[1].split("]")[0]
	splitcoords = coords.split(",")
	latitude = float(splitcoords[2])
	longitude = float(splitcoords[1])
	return([latitude, longitude])

name = input()
print(get_coords(name))