import sys
import pprint
# takes in food data
# food name, protein, fat, carb, fiber (per 100g)
# returns a map of {K=food, V=[nutrition]}

DEFAULT_SERVING_SIZE = 100
NUTRIENT_ARRAY = ["Protein", "Carb", "Fat", "Fiber"]
CALS_PER_NUTRIENT = [4,4,9,0]

#TODO replace these with functions
TARGET_NUTRITION = [200, 200, 40, 20]
TARGET_CALS = 0
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
def add_food_to_total(food, serving_size_grams, food_library, total):
	assert food in food_library.keys()

	food_arr = food_library[food]

	cal_in_food = 0
	for i in range(len(NUTRIENT_ARRAY)):
		nutrient_per_serving_size = food_arr[i]
		nutrient_total = float(nutrient_per_serving_size) / DEFAULT_SERVING_SIZE * serving_size_grams
		#TODO this is brittle... should we check which nutrient we're parsing?
		total[i] += nutrient_total
		cal_in_food += CALS_PER_NUTRIENT[i] * nutrient_total

	return cal_in_food


with open(sys.argv[1], "rtU") as f:
	food_library = parse_food_file_into_data_structure(f)

	total = [0] * len(NUTRIENT_ARRAY)
	total_cal = 0
	total_cal += add_food_to_total("chicken breast", 300, food_library, total)
	total_cal += add_food_to_total("avocado", 220, food_library, total)
	total_cal += add_food_to_total("broccoli", 500, food_library, total)

	for i in range(len(NUTRIENT_ARRAY)):
		print(NUTRIENT_ARRAY[i] + ": " + str(total[i]) + " Remaining: " + str(TARGET_NUTRITION[i] - total[i]))

	print ("Calories: " + str(total_cal) + " Remaining: " + str(TARGET_CALS - total_cal))


# target nutrition; remaining nutrition for the day.
# target cals, remaining cals for the day.
# meal's percentage of cals by macro





#1. Query document to build up list of foods with their nutrition info
#2. Command line prompt loop -> prompt for which food and how much grams of it until done entering a meal
#3. print out summary and ask "is this correct?"
#4. print out meal summary: nutrition per meal (fat, carbs, protein, fiber) & calorie breakdown

#5. "What's left for the day?" Given calorie target (hardcoded) and macro target (hardcoded), tell you what you have left after this meal
#6. keep track of the day: Start morning off with calorie and macro target. Program stores state of what was eaten and what is left. On next meal it continues that state. Based on date/time

#7. type-ahead search for foods

#8. save a daily human readable summary (what foods, what macros hit, total cals)






