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

	def __str__(self):
		return str(self.serving_size) + "g " + self.name 


# TODO, can methods here be static?
class FoodFactory():
	def __init__(self, food_library):
		self.food_library = food_library

	def create_food(self, name, serving_size):
		assert name in self.food_library.keys()
		nutrition = self.food_library[name]
		serving_size = int(serving_size)
		food = Food(name, serving_size, [float(n) * serving_size / DEFAULT_SERVING_SIZE for n in nutrition])
		return food



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

	def add_food(self, food):
		self.foods.append(food)

	def __str__(self):
		ret = ""
		for food in self.foods:
			ret+= str(food) + "\n"
		return ret


def parse_food_file_into_data_structure(f):
	data = {}
	for line in f: 
		food_arr = line.strip().split(',')
		assert len(food_arr) == len(NUTRIENT_ARRAY) + 1

		#TODO more assertions for input structure
		data[food_arr[0]] = food_arr[1:]

	return data


def food_prompt_loop(foodFactory):
	meal = Meal()
	while True: 
		more_input = raw_input("Enter a food? ")
		if more_input == "n":
			break
		#TODO make assertion for food happen here
		food = raw_input("What food? ").strip()
		#TODO bake int type into prompt
		serving_size = raw_input("Amount: ")

		meal.add_food(foodFactory.create_food(food, int(serving_size)))

		#TODO figure out how to limit input to y/n
		#TODO figure out how to not ask this question every time, and instead have an opportunity to escape the food loop


	# check if meal is correct
	print(meal)
	correct = raw_input("Is this correct? ")

	#TODO bake this into prompt
	#assert correct == "y"

	return meal


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


def main():
	#TODO use cmd line parser instead of this
	#TODO figure out how to not have 2 nested scopes
	with open(sys.argv[1], "rtU") as food_library_file:
		food_library = parse_food_file_into_data_structure(food_library_file)
		foodFactory = FoodFactory(food_library)

		meal = food_prompt_loop(foodFactory)

		write_to_foodlog(sys.argv[2], meal)

		meals = parse_food_log(sys.argv[2], foodFactory)

		for m in meals:
			print(m)
	# 	with open(sys.argv[2], "a") as food_log:


def parse_food_log(food_log_file_name, foodFactory):
	meals = []
	with open(food_log_file_name, "rtU") as food_log:
		meal = Meal()
		for line in food_log:			
			#TODO better way to delimit?
			if '*' in line:
				meals.append(meal)
				meal = Meal()
			else:
				food_and_serving_size = line.strip().split(',')
				print(food_and_serving_size)
				assert len(food_and_serving_size) == 2
				food = foodFactory.create_food(food_and_serving_size[0], food_and_serving_size[1])
				meal.add_food(food)
	return meals

def write_to_foodlog(food_log_file_name, meal):
	if len(meal.foods) == 0:
		return

	with open(food_log_file_name, "a") as food_log:
		for food in meal.foods:
			food_log.write(food.name + "," + str(food.serving_size) + "\n")
		#TODO better way for meal delimiter?
		food_log.write("*\n")

#TODO can I use cmd line parser for file name args?
main()
#with open(sys.argv[1], "rtU") as f:
	#food_library = parse_food_file_into_data_structure(f)

	#meal = Meal()

	#food_prompt_loop(food_library, meal)
#	add_food_to_meal("chicken breast", 300, food_library, meal)
#	add_food_to_meal("avocado", 220, food_library, meal)
#	add_food_to_meal("broccoli", 500, food_library, meal)

	# Write meal to file

	# for meal in all_meals_in_above_file: 
	#print_meal_stats(meal)
	# running counter for daily and remaining nurition/cals

	#TODO print Day's Total

# target nutrition; remaining nutrition for the day.
# target cals, remaining cals for the day.
# meal's percentage of cals by macro

#1. write each meal to a file
#2. parse all meals from the mega file
#3. figure out how to end the day
#4. prompt user in a loop for entering foods
#5.

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






