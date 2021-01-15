import time
from os import path

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from pyswip import Prolog



fullPlFile = "consolidated.pl"


def sanitize(passed):
	passed = passed.replace("!", "")
	passed = passed.replace("<", "")
	passed = passed.replace("'", "")
	passed = passed.replace(">", "")
	passed = passed.replace(";", "")
	passed = passed.replace("?", "")
	passed = passed.replace("#", "")
	passed = passed.replace(".", "")
	passed = passed.replace("\\", "")
	passed = passed.replace("/", "")
	return passed

def getHTMLContent(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
	try:
		with closing(get(url, headers=headers)) as resp:
			return resp.content

	except e:
		print("An error", str(e), "occurred!")
		return None

def get_coords(locationPassed):
	locationPassed = sanitize(locationPassed)
	locationPassed = locationPassed.replace(" " , "+")
	print("location passed is:", locationPassed)
	mapContent = str(getHTMLContent("https://www.google.com/maps/place/" + locationPassed))
	#mapContent = str(getHTMLContent("https://www.google.com/maps/search/?api=1&query=" + locationPassed))
	
	if "window.APP_INITIALIZATION_STATE=[[[" not in mapContent:
		return None
	coords = mapContent.split("window.APP_INITIALIZATION_STATE=[[[")[1].split("]")[0]
	splitcoords = coords.split(",")
	latitude = float(splitcoords[2])
	longitude = float(splitcoords[1])
	print("coords are", [latitude, longitude])
	return([latitude, longitude])
	
def pl_safe(passed):
	passed = passed.lower()
	passed = passed.replace(" ", "")
	return passed
	
def big_letters(passed):
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
	prolog = Prolog()
	prolog.consult(fullPlFile)
	if passed == None:
		return None
	food_nationalities = []
	for keyword in passed:
		for result in list(prolog.query("nation_to_nationality("+keyword+", NATIONALITY); continent_to_adjective("+keyword+", NATIONALITY).")):
			food_nationalities.append(result["NATIONALITY"])
	
	return food_nationalities
	
def get_restaurants_per_page(userid):
	prolog = Prolog()
	prolog.consult(fullPlFile)
	result = list(prolog.query("restaurantsPerPage("+userid+", R)"))
	if len(result) == 0:
		return -1
	return int(result[0]["R"])
	
def is_small_business_mode(userid):
	prolog = Prolog()
	prolog.consult(fullPlFile)
	result = list(prolog.query("restaurantsPerPage("+userid+", R)"))
	if len(result) == 0:
		return False
	return int(result[0]["R"]) == 1

def first_time_setup(userid):
	userfile = open(userid+".pl", "w")
	userfile.write("%user_location_line\n")
	userfile.write("coordinates("+userid+"_location, 32.98576190000001, -96.7500993).\n")
	userfile.write("%rest_per_page_line\n")
	userfile.write("restaurantsPerPage("+userid+", 5).\n")
	userfile.write("%small_business_line\n")
	userfile.write("smallBusinessMode("+userid+", 1).\n")
	userfile.close()
	
	pfilehandler = open(fullPlFile, "a")
	pfilehandler.write(":- ["+userid+"].\n")
	pfilehandler.close()
	
	print("default setting: ", get_restaurants_per_page(userid))	
	
def new_coordinates(userid, coordsarray):
	userfile = open(userid+".pl", "r")
	filelines = userfile.readlines()
	userfile.close()
	userfile = open(userid+".pl", "w")
	onLocationLine = False
	for line in filelines:
		if onLocationLine:
			userfile.write("coordinates("+userid+"_location, "+str(coordsarray[0])+", "+str(coordsarray[1])+").\n")
			onLocationLine = False
		else:
			userfile.write(line)
		if line.strip() == "%user_location_line":
			onLocationLine = True
	userfile.close()
	print("Successfully updated your location!")
	
	
def update_rest_per_page(userid, newrpp):
	userfile = open(userid+".pl", "r")
	filelines = userfile.readlines()
	userfile.close()
	userfile = open(userid+".pl", "w")
	onRppLine = False
	for line in filelines:
		if onRppLine:
			userfile.write("restaurantsPerPage("+userid+", "+str(newrpp)+").\n")
			onRppLine = False
		else:
			userfile.write(line)
		if line.strip() == "%rest_per_page_line":
			onRppLine = True
	userfile.close()
	print("Successfully updated your restaurants per page!")
	
def update_small_business_settings(userid, mode):
	userfile = open(userid+".pl", "r")
	filelines = userfile.readlines()
	userfile.close()
	userfile = open(userid+".pl", "w")
	onSbsLine = False
	for line in filelines:
		if onSbsLine:
			userfile.write("smallBusinessMode("+userid+", "+str(newrpp)+").\n")
			onSbsLine = False
		else:
			userfile.write(line)
		if line.strip() == "%small_business_line":
			onSbsLine = True
	userfile.close()
	print("Successfully updated your small business settings!")
	
def help():
	print("help menu placeholder")

def list_error():
	print("Error: you must format the list command as one of the following:")
	print("List restaurants within <number> miles.")
	print("List <type> restaurants within <number> miles.")
	print("List restaurants between <lower> and <upper> ratings.")
	print("List <type> restaurants between <lower> and <upper> ratings.")
	
def print_list(list_passed, userid):
	list_i = 0
	rests_per_page = get_restaurants_per_page(userid)
	while list_i < len(list_passed):
		for q in range(rests_per_page):
			if list_i + q >= len(list_passed):
				break
			
def list_category_restaurants_in_range(userid, rest_range, categorizer):
	prolog = Prolog()
	prolog.consult(fullPlFile)
	result = list(prolog.query("get_restaurant_range_distance_list_with_category("+userid+"_location, "+str(rest_range)+", A, "+categorizer+"), sort_by_distance(A, ANSWER)"))
	if len(result) == 0:
		print("No restaurants were found in that range!")
	else:
		resultlist = result[0]["ANSWER"]
		list_i = 0
		rests_per_page = get_restaurants_per_page(userid)
		while list_i < len(resultlist):
			print("---------------")
			print("Results "+ str(list_i + 1) + "-" + str(min(list_i + rests_per_page, len(resultlist))) + " out of", len(resultlist))
			for q in range(rests_per_page):
				if list_i + q >= len(resultlist):
					break
				print(str(list_i + q + 1) + ".",big_letters(resultlist[list_i + q].args[0].value), " (distance", round(resultlist[list_i + q].args[1], 2), "miles)")
			nextput = input("Type 'next' to see the next " + str(rests_per_page) + " results, or 'quit' to stop showing more results: ")
			while nextput.lower() != "next" and nextput.lower() != "quit":
				nextput = input("Type 'next' to see the next " + str(rests_per_page) + " results, or 'quit' to stop showing more results: ")
			if nextput.lower() == "next":
				list_i += rests_per_page
			else:
				break
				
def list_restaurants_in_range(userid, rest_range):
	prolog = Prolog()
	prolog.consult(fullPlFile)
	result = list(prolog.query("get_restaurant_range_distance_list("+userid+"_location, "+str(rest_range)+", A), sort_by_distance(A, ANSWER)"))
	if len(result) == 0:
		print("No restaurants were found in that range!")
	else:
		resultlist = result[0]["ANSWER"]
		list_i = 0
		rests_per_page = get_restaurants_per_page(userid)
		while list_i < len(resultlist):
			print("---------------")
			print("Results "+ str(list_i + 1) + "-" + str(min(list_i + rests_per_page, len(resultlist))) + " out of", len(resultlist))
			for q in range(rests_per_page):
				if list_i + q >= len(resultlist):
					break
				print(str(list_i + q + 1) + ".",big_letters(resultlist[list_i + q].args[0].value), " (distance", round(resultlist[list_i + q].args[1], 2), "miles)")
			nextput = input("Type next to see the next " + str(rests_per_page) + " results, or quit to stop showing more results: ")
			while nextput.lower() != "next" and nextput.lower() != "quit":
				nextput = input("Type next to see the next " + str(rests_per_page) + " results, or quit to stop showing more results: ")
			if nextput.lower() == "next":
				list_i += rests_per_page
			else:
				break
	
def list_ratings_restaurants_in_range(userid, lower, upper, categorizer):
	prolog = Prolog()
	prolog.consult(fullPlFile)
	#print("got here too")
	result = list(prolog.query("get_restaurant_rating_list_with_category("+categorizer+", "+str(lower)+", "+str(upper)+",  A), sort_by_ratings(A, ANSWER)"))
	if len(result) == 0:
		print("No restaurants were found in that range!")
	else:
		resultlist = result[0]["ANSWER"]
		list_i = 0
		rests_per_page = get_restaurants_per_page(userid)
		while list_i < len(resultlist):
			print("---------------")
			print("Results "+ str(list_i + 1) + "-" + str(min(list_i + rests_per_page, len(resultlist))) + " out of", len(resultlist))
			for q in range(rests_per_page):
				if list_i + q >= len(resultlist):
					break
				print(str(list_i + q + 1) + ".",big_letters(resultlist[list_i + q].args[0].value), " (rating", round(resultlist[list_i + q].args[1], 2), ")")
			nextput = input("Type 'next' to see the next " + str(rests_per_page) + " results, or 'quit' to stop showing more results: ")
			while nextput.lower() != "next" and nextput.lower() != "quit":
				nextput = input("Type 'next' to see the next " + str(rests_per_page) + " results, or 'quit' to stop showing more results: ")
			if nextput.lower() == "next":
				list_i += rests_per_page
			else:
				break
	
def list_ratings_small_businesses_in_range(userid, lower, upper, categorizer):
	prolog = Prolog()
	prolog.consult(fullPlFile)
	result = list(prolog.query("get_small_business_rating_list_with_category("+categorizer+", "+str(lower)+", "+str(upper)+",  A), sort_by_ratings(A, ANSWER)"))
	if len(result) == 0:
		print("No restaurants were found in that range!")
	else:
		resultlist = result[0]["ANSWER"]
		list_i = 0
		rests_per_page = get_restaurants_per_page(userid)
		while list_i < len(resultlist):
			print("---------------")
			print("Results "+ str(list_i + 1) + "-" + str(min(list_i + rests_per_page, len(resultlist))) + " out of", len(resultlist))
			for q in range(rests_per_page):
				if list_i + q >= len(resultlist):
					break
				print(str(list_i + q + 1) + ".",big_letters(resultlist[list_i + q].args[0].value), " (rating", round(resultlist[list_i + q].args[1], 2), ")")
			nextput = input("Type 'next' to see the next " + str(rests_per_page) + " results, or 'quit' to stop showing more results: ")
			while nextput.lower() != "next" and nextput.lower() != "quit":
				nextput = input("Type 'next' to see the next " + str(rests_per_page) + " results, or 'quit' to stop showing more results: ")
			if nextput.lower() == "next":
				list_i += rests_per_page
			else:
				break
				
def main():
	username = input("Enter username: ")
	username = sanitize(username)
	userid = sanitize(username).lower()
	if not path.exists(userid+".pl"):
		print("New user detected, setting up your profile...")
		first_time_setup(userid)
	else:
		print("Welcome back," username,"!")
	print("Welcome to Hungry, Hungry, Homey! Type help to view all commands")
	
	while True:
		print("")
		print("---------------")
		print("")
		userput = input().lower()
		splitput = userput.split(" ")
		command = splitput[0]
		if command == "help":
			help()
		elif command == "end":
			break
		elif command == "list":
			sbmcheck = is_small_business_mode(userid)
			if "restaurants" not in userput:
				list_error()
			else:
				categorizer = ""
				currentI = 1
				while currentI < len(splitput) and splitput[currentI] != "restaurants":
					categorizer += splitput[currentI] + " "
					currentI += 1
				categorizer.strip()
				categorizer = pl_safe(categorizer)
				if len(categorizer) == 0:
					rest_range = splitput[-2]
					try:
						rest_range = float(rest_range)
						list_restaurants_in_range(userid, rest_range)
						
						
					except:
						list_error()
				else:
					if 'miles' not in userput and 'ratings' not in userput:
						list_error()
					else:
						if 'miles.' == splitput[-1]:
							rest_range = splitput[-2]
							try:
								rest_range = float(rest_range)
								list_category_restaurants_in_range(userid, rest_range, categorizer)
							except:
								list_error()
						else:
							lower = splitput[-4]
							upper = splitput[-2]
							#print("lower:", lower, "and upper:", upper)
							
							try:
								lower = float(lower)
								upper = float(upper)
								if not sbmcheck:
									list_ratings_restaurants_in_range(userid, lower, upper, categorizer)
								else:
									list_ratings_small_businesses_in_range(userid, lower, upper, categorizer)
							except:
								list_error()
							'''
							lower = float(lower)
							upper = float(upper)
							#list_ratings_restaurants_in_range(userid, lower, upper, categorizer)
							list_ratings_small_businesses_in_range(userid, lower, upper, categorizer)
							'''
							
						
		elif command == "location":
			if len(splitput) == 1:
				print("Error: you must supply a location!")
			else:
				location = userput[9:]
				coordarr = get_coords(location)
				if coordarr == None:
					print("Error: invalid location!")
				else:
					new_coordinates(userid, coordarr)
		
		elif command == "enjoy":
			food_type_lines = []
			food_category_lines = []
			food_name_input = None
			if len(splitput) == 1:
				print("Error: you must supply the food you enjoy!")
			else:
				food_name_input = userput[6:]
				food_name_input = pl_safe(food_name_input)
				
				food_type = get_food_type(food_name_input)
				if food_type is not None:
					food_type = pl_safe(food_type)
					food_type_lines.append('equate_food_name({}, {}).\n'.format(food_name_input, food_type))
					foodnatarr = get_food_nationality(get_food_nation(food_name_input))
					for nationality in foodnatarr:
						food_category_lines.append('equate_food_name({}, {}).\n'.format(food_name_input, nationality))
						
					userfile = open(userid+".pl", "a")
					
					userfile.write("enjoysFood("+userid+", "+food_name_input+").\n")
					userfile.close()
					print("Added food preferences for", food_name_input)
					print("Here are suggestions based off that food")
					list_ratings_restaurants_in_range(userid, 3.0, 5.0, nationality)
		

	
if __name__ == "__main__":
	main()