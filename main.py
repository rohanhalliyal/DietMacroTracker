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

class Food():
	def __init__(self, name, serving_size, nutrition):
		self.name = name
		self.serving_size = serving_size
		self.nutrition = nutrition

	def get_calories(self): 
		total_cal = 0
		for i in range(len(NUTRIENT_ARRAY)):
			total_cal += CALS_PER_NUTRIENT[i] * self.nutrition[i]
		return total_cal


class Meal():
	def __init__(self):
		self.foods = []

	def get_total_calories(self):
		total_cal = 0
		for food in self.foods:
			total_cal += food.get_calories()

		return total_cal

	def get_total_nutrition(self):
		total_nutrition = [0] * len(NUTRIENT_ARRAY)
		for food in self.foods:
			#TODO (make each nutrient be a first class member of FOod)
			for i in range(len(NUTRIENT_ARRAY)):
				total_nutrition[i] += food.nutrition[i]

		return total_nutrition

	def add_food(self, food_name, nutrition_value, serving_size):
		# TODO not needed -> assert food_name not in self.foods
		food = Food(food_name, serving_size, [float(n) * serving_size / 100 for n in nutrition_value])
		self.foods.append(food)


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


def add_food_to_meal(food, serving_size_grams, food_library, meal):
	assert food in food_library.keys()
	food_arr = food_library[food]
	meal.add_food(food, food_arr, serving_size_grams)


def print_meal_stats(meal_stats):
	for food in meal.foods:
		str_to_print = str(food.serving_size) + " grams " + food.name + ": "
		for i in range(len(NUTRIENT_ARRAY)):
			str_to_print += NUTRIENT_ARRAY[i] + " " + str(food.nutrition[i]) + "g "
		print(str_to_print)

	str_to_print = "Meal Total: "
	for i in range(len(NUTRIENT_ARRAY)):
		str_to_print += NUTRIENT_ARRAY[i] + " " + str(meal.get_total_nutrition()[i]) + "g "
	print(str_to_print)

with open(sys.argv[1], "rtU") as f:
	food_library = parse_food_file_into_data_structure(f)

	meal = Meal()
	add_food_to_meal("chicken breast", 300, food_library, meal)
	add_food_to_meal("avocado", 220, food_library, meal)
	add_food_to_meal("broccoli", 500, food_library, meal)

	# Write meal to file

	# for meal in all_meals_in_above_file: 
	print_meal_stats(meal)
	# running counter for daily and remaining nurition/cals

	#TODO print Day's Total

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






