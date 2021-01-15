:- multifile(coordinates/3).
:- multifile(enjoysFood/2).
:- multifile(enjoysRestaurant/2).
:- multifile(restaurantsPerPage/2).


:- [restaurant_categories].

:- [restaurant_ratings].

:- [restaurant_is_open].


:- [restaurant_coordinates].

:- [small_businesses].

:- [nationalities].

:- [food_types].


distance(L1, L2, X) :- coordinates(L1, X1, Y1),
    coordinates(L2, X2, Y2),
    X is sqrt((X2 - X1)^2 + (Y2 - Y1)^2).

first_rating(RESTAURANT, RATING) :- rating(RESTAURANT, RATING), !.

get_restaurants_in_rating_range(LOW, HIGH, RESTAURANT) :- rating(RESTAURANT, RATING), RATING >= LOW, RATING =< HIGH.

get_restaurants_in_rating_range_and_r(LOW, HIGH, RESTAURANT, RATING) :- rating(RESTAURANT, RATING), RATING >= LOW, RATING =< HIGH.

get_restaurants_in_rating_range_with_category(CATEGORY, LOW, HIGH, RESTAURANT, RATING) :- rating(RESTAURANT, RATING), RATING >= LOW, RATING =< HIGH, category(RESTAURANT, CATEGORY).

get_restaurant_rating_list_with_category(CATEGORY, LOW, HIGH, ANSWER) :- findall((RESTAURANT, RATING), 
	get_restaurants_in_rating_range_with_category(CATEGORY, LOW, HIGH, RESTAURANT, RATING), ANSWER).

get_small_business_rating_list_with_category(CATEGORY, LOW, HIGH, ANSWER) :- findall((RESTAURANT, RATING), 
	(get_restaurants_in_rating_range_with_category(CATEGORY, LOW, HIGH, RESTAURANT, RATING), is_small_business(RESTAURANT))
	, ANSWER).
	
get_restaurant_rating_list(LOW, HIGH, ANSWER) :- findall((RESTAURANT, RATING), 
	get_restaurants_in_rating_range_and_r(LOW, HIGH, RESTAURANT, RATING), ANSWER).

get_restaurants_in_range(SOURCE, RESTAURANT, RANGE, ACTUAL_DISTANCE) :- CALCULATED_RANGE is 0.0144927536 * RANGE,
    distance(SOURCE, RESTAURANT, X), not(=(SOURCE, RESTAURANT)), X =< CALCULATED_RANGE, ACTUAL_DISTANCE is X * 69.

get_restaurants_in_range_with_category(SOURCE, RESTAURANT, CATEGORY, RANGE, ACTUAL_DISTANCE) :- CALCULATED_RANGE is 0.0144927536 * RANGE,
    distance(SOURCE, RESTAURANT, X), not(=(SOURCE, RESTAURANT)), X =< CALCULATED_RANGE, ACTUAL_DISTANCE is X * 69, category(RESTAURANT, CATEGORY).

	
get_restaurant_range_distance_list(SOURCE, RANGE, ANSWER) :- findall((RESTAURANT, ACTUAL_DISTANCE), get_restaurants_in_range(SOURCE, RESTAURANT, RANGE, ACTUAL_DISTANCE), ANSWER).

get_small_business_range_distance_list(SOURCE, RANGE, ANSWER)
	:- findall((RESTAURANT, ACTUAL_DISTANCE),
	(get_restaurants_in_range(SOURCE, RESTAURANT, RANGE, ACTUAL_DISTANCE), is_small_business(RESTAURANT)),
	ANSWER).


get_restaurant_range_distance_list_with_category(SOURCE, RANGE, ANSWER, CATEGORY) :- findall((RESTAURANT, ACTUAL_DISTANCE), get_restaurants_in_range_with_category(SOURCE, RESTAURANT, CATEGORY, RANGE, ACTUAL_DISTANCE), ANSWER).

get_small_business_range_distance_list_with_category(SOURCE, RANGE, ANSWER, CATEGORY)
	:- findall((RESTAURANT, ACTUAL_DISTANCE),
	(get_restaurants_in_range_with_category(SOURCE, RESTAURANT, CATEGORY, RANGE, ACTUAL_DISTANCE), is_small_business(RESTAURANT)), ANSWER).


get_restaurant_range_list(SOURCE, RANGE, ANSWER) :- findall(RESTAURANT, get_restaurants_in_range(SOURCE, RESTAURANT, RANGE, _), ANSWER).


get_food_suggestions(FOOD, SUGGESTED_RESTAURANT) :- equate_food_type(FOOD, TYPE),
	category(SUGGESTED_RESTAURANT, TYPE); food_category(FOOD), category(SUGGESTED_RESTAURANT, FOOD).



%functions_to_sort_restaurants
	
greater_distance(ONE, TWO) :- (_, D1) = ONE, 
    (_, D2) = TWO,
    D1 > D2 -> true();
    (_, D1) = ONE, 
    (_, D2) = TWO,
    D1 =< D2 -> false().

sort_by_distance(LIST, RESULT) :-
    (LIST = []; LIST = [_]) ->  
    RESULT = LIST;
    LIST = [PIVOT | TAIL],
	classify(greater_distance(PIVOT), TAIL, LEFT, RIGHT),
    sort_by_distance(LEFT, SORTEDLEFT),
    sort_by_distance(RIGHT, SORTEDRIGHT),
    join_lists(SORTEDLEFT, [PIVOT], FIRSTJOIN),
    join_lists(FIRSTJOIN, SORTEDRIGHT, RESULT).

lesser_rated(ONE, TWO) :- (_, R1) = ONE, 
    (_, R2) = TWO,
    R1 < R2 -> true();
    (_, R1) = ONE, 
    (_, R2) = TWO, 
    R1 >= R2 -> false().

sort_by_ratings(LIST, RESULT) :-
    (LIST = []; LIST = [_]) ->  
    RESULT = LIST;
    LIST = [PIVOT | TAIL],
	classify(lesser_rated(PIVOT), TAIL, LEFT, RIGHT),
    sort_by_ratings(LEFT, SORTEDLEFT),
    sort_by_ratings(RIGHT, SORTEDRIGHT),
    join_lists(SORTEDLEFT, [PIVOT], FIRSTJOIN),
    join_lists(FIRSTJOIN, SORTEDRIGHT, RESULT).

join_lists(LISTONE,LISTTWO, RESULT) :-
    reverse_list(LISTONE, [], REV_ONE),
    reverse_list(REV_ONE, LISTTWO, RESULT).


reverse_list(LISTONE, ACC, RESULT) :-
    LISTONE = [] ->  
    RESULT = ACC, !;
	LISTONE = [HEAD | TAIL],
    NEWACC = [HEAD | ACC],
    reverse_list(TAIL, NEWACC, RESULT).


classify(CLASSIFIER, LIST, LISTONE, LISTTWO) :-
    LIST = [] -> 
		LISTONE = [],
		LISTTWO = [];
    LIST = [HEAD | TAIL],
    call(CLASSIFIER, HEAD) -> 
		classify(CLASSIFIER, TAIL, NEWERONE, NEWERTWO),
		LISTONE = [HEAD | NEWERONE],
		LISTTWO = NEWERTWO;
    LIST = [HEAD | TAIL], 
	classify(CLASSIFIER, TAIL, NEWERONE, NEWERTWO),
	LISTTWO =[HEAD | NEWERTWO],
	LISTONE = NEWERONE.

%userdata


:- [akbara]