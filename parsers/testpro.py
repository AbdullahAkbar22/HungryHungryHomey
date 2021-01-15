from pyswip import Functor, Variable, Query, call, Prolog

prolog = Prolog()
prolog.consult("consolidated.pl")

restaurantRange = input("Enter restaurant range (miles):")

		
		
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


result = list(prolog.query("get_restaurants_in_range(my_house, R, "+restaurantRange+", X)."))
for soln in result:
	print(bigLetters(soln["R"]), "which is", soln["X"], "miles away.")