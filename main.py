import sys
import pprint
# takes in food data
# food name, protein, fat, carb, fiber (per 100g)
# returns a map of {K=food, V=[nutrition]}

pp = pprint.PrettyPrinter(indent=4)

DEFAULT_SERVING_SIZE = 100
NUTRIENT_ARRAY = ["Protein", "Carb", "Fat", "Fiber"]
CALS_PER_NUTRIENT = [4,4,9,0]

#TODO replace these with functions
TARGET_NUTRITION = [200, 200, 40, 20]
TARGET_CALS = 0

#TODO replace with ENUM
CALORIES = "Calories"
NUTRITION = "Nutrition"
FOODS = "FOODS"

for i in range(len(TARGET_NUTRITION)):
	TARGET_CALS += TARGET_NUTRITION[i] * CALS_PER_NUTRIENT[i]


def parse_food_file_into_data_structure(f):
	data = {}
	for line in f: 
		food_arr = line.strip().split(',')
		assert len(food_arr) == len(NUTRIENT_ARRAY) + 1

		#TODO more assertions for input structure
		data[food_arr[0]] = food_arr[1:]

	return data

def food_prompt_loop():
	# spin up prompt for user to input
	# collect input with running total

	pass

# total data structure, [protein, carb, fat, fiber]
def add_food_to_meal(food, serving_size_grams, food_library, meal_stats):
	assert food in food_library.keys()

	food_arr = food_library[food]

	cal_in_food = 0
	meal_stats[FOODS][food] = (serving_size_grams, [0] * len(NUTRIENT_ARRAY))
	for i in range(len(NUTRIENT_ARRAY)):
		nutrient_per_serving_size = food_arr[i]
		nutrient_total = float(nutrient_per_serving_size) / DEFAULT_SERVING_SIZE * serving_size_grams
		#TODO this is brittle... should we check which nutrient we're parsing?
		meal_stats[FOODS][food][1][i] = nutrient_total
		meal_stats[NUTRITION][i] += nutrient_total
		meal_stats[CALORIES] += CALS_PER_NUTRIENT[i] * nutrient_total


	#TODO ignored
	return meal_stats

def print_meal_stats(meal_stats):
	for food in meal_stats[FOODS]:
		str_to_print = str(meal_stats[FOODS][food][0]) + " grams " + food + ": "
		for i in range(len(NUTRIENT_ARRAY)):
			str_to_print += NUTRIENT_ARRAY[i] + " " + str(meal_stats[FOODS][food][1][i]) + "g "
		print(str_to_print)

	str_to_print = "Meal Total: "
	for i in range(len(NUTRIENT_ARRAY)):
		str_to_print += NUTRIENT_ARRAY[i] + " " + str(meal_stats[NUTRITION][i]) + "g "
	print(str_to_print)

with open(sys.argv[1], "rtU") as f:
	food_library = parse_food_file_into_data_structure(f)

	meal_stats = {CALORIES: 0, NUTRITION: [0] * len(NUTRIENT_ARRAY), FOODS: {}}
	add_food_to_meal("chicken breast", 300, food_library, meal_stats)
	add_food_to_meal("avocado", 220, food_library, meal_stats)
	add_food_to_meal("broccoli", 500, food_library, meal_stats)

	# Write meal to file

	print_meal_stats(meal_stats)

	#TODO print Day's Total

	str_to_print = "Remaining: "
		#print(meal_stats[FOODS][food])
	#for i in range(len(NUTRIENT_ARRAY)):
	#	print(NUTRIENT_ARRAY[i] + ": " + str(meal_stats[NUTRITION][i]) + " Remaining: " + str(TARGET_NUTRITION[i] - meal_stats[NUTRITION][i]))

	#print ("Calories: " + str(meal_stats[CALORIES]) + " Remaining: " + str(TARGET_CALS - meal_stats[CALORIES]))


# target nutrition; remaining nutrition for the day.
# target cals, remaining cals for the day.
# meal's percentage of cals by macro

# 1. how to open and write to a file permanently
# 1b. Alternatively, use a DB
# 2. How to prompt user in a loop

# BRAINSTORM
# WHAT TO WRITE TO FILE: food serving_size, food serving_size, NEXT MEAL, food serving_size etc
# then prase the entire file, give breakdown by MEAL 1: MEAL 2: MEAL 3: etc

# MEAL#1
# chicken breast 100g      Protein: 50g. Carb 40g. Fat 20g. Fiber 0g.
# avocado        100g      Protein: 50g. Carb 40g. Fat 20g. Fiber 0g.
# sweet potato   100g      Protein: 50g. Carb 40g. Fat 20g. Fiber 0g.
# total                    Protein 150g. Carb 120g. Fat 60g. Fiber 0g. Cals 1000. 
# remaining: 			   Protein 30g. Carb 46g. Fat 20g. Fiber 40g. Cals 800
# MEAL #2



# Assume which date ( Today ) that the food is for, but ask if user wants to change it


#1. Query document to build up list of foods with their nutrition info
#2. Command line prompt loop -> prompt for which food and how much grams of it until done entering a meal
#3. print out summary and ask "is this correct?"
#4. print out meal summary: nutrition per meal (fat, carbs, protein, fiber) & calorie breakdown

#5. "What's left for the day?" Given calorie target (hardcoded) and macro target (hardcoded), tell you what you have left after this meal
#6. keep track of the day: Start morning off with calorie and macro target. Program stores state of what was eaten and what is left. On next meal it continues that state. Based on date/time

#7. type-ahead search for foods

#8. save a daily human readable summary (what foods, what macros hit, total cals)






