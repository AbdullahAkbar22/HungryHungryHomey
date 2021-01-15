import time

from requests import get
from requests.exceptions import RequestException
from contextlib import closing

def getHTMLContent(url):
	#headers = {'User-Agent': 'Mozilla/5.0'}
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
		finalword += word[0].upper() + word[1:]
		if i != len(splitword) - 1:
			finalword += " "
	return finalword
	
def is_small_business(passed):
	htmlBody = str(getHTMLContent("https://google.com/search?q=" + passed + " restaurant"))
	print(htmlBody)
	time.sleep(1)
	if 'class="kno-rdesc"' in htmlBody:
		return False
	return True



name = input()
print(is_small_business(name))