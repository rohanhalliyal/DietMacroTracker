import sys
import pprint 
import argparse
import datetime

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


#TODO re-write using a lambda
def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Use y/n:")


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
	while yes_or_no("Enter a food?"): 
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

def build_nutrition_string(nutrition):
	str_to_print = ""
	for i in range(len(NUTRIENT_ARRAY)):
		str_to_print += NUTRIENT_ARRAY[i] + " " + str(nutrition[i]) + "g "
	return str_to_print

def print_meal_stats(meal):
	for food in meal.foods:
		str_to_print = str(food.serving_size) + " grams " + food.name + ": "
		for i in range(len(NUTRIENT_ARRAY)):
			str_to_print += NUTRIENT_ARRAY[i] + " " + str(food.nutrition[i]) + "g "
		print(str_to_print)

	print "Meal Total: {}Calories: {}\n".format(build_nutrition_string(meal.get_total_nutrition()), meal.get_total_calories())

def print_total_nutrition(meals):
	total_calories = 0
	total_nutrition = [0] * len(NUTRIENT_ARRAY)
	for meal in meals:
		total_calories += meal.get_total_calories()
		for i in range(len(total_nutrition)):
			total_nutrition[i] += meal.get_total_nutrition()[i]
	
	remaining_nutrition = [0] * len(NUTRIENT_ARRAY)
	for i in range(len(total_nutrition)):
		remaining_nutrition[i] = TARGET_NUTRITION[i] - total_nutrition[i]

	print
	print "Nutrition: {}Calories: {}".format(build_nutrition_string(total_nutrition), total_calories)
	print "Remaining: {}Calories: {}".format(build_nutrition_string(remaining_nutrition), TARGET_CALS - total_calories)


def main():	
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--library", 
		required=False, 
		nargs=1, 
		default='food_spreadsheet.csv',
		dest="food_library_file",
		type=file,
		action='store',
		help='File path of possible foods and their nutritional values')

	parser.add_argument(
		"--log",
		nargs=1,
		required=False,
		default='food_logs/{}.txt'.format(datetime.datetime.now().strftime("%Y-%m-%d")),
		dest='food_log_file',
		action='store',
		help='File path of food log file to use')


	args = parser.parse_args()

	if not yes_or_no("Will use library '{}' and log '{}'".format(
		args.food_library_file.name, 
		args.food_log_file)
	):
		parser.print_help()
		return

	food_library = parse_food_file_into_data_structure(args.food_library_file)

	foodFactory = FoodFactory(food_library)

	meal = food_prompt_loop(foodFactory)

	write_to_foodlog(args.food_log_file, meal)

	meals = parse_food_log(args.food_log_file, foodFactory)

	for i in range(len(meals)):
		print "Meal {}:".format(i)
		print_meal_stats(meals[i])

	print_total_nutrition(meals)


def parse_food_log(food_log_file_name, foodFactory):
	meals = []
	#TODO try catch
	with open(food_log_file_name, "rtU") as food_log:
		meal = Meal()
		for line in food_log:			
			#TODO better way to delimit?
			if '*' in line:
				meals.append(meal)
				meal = Meal()
			else:
				food_and_serving_size = line.strip().split(',')
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

# 2. default file choices for food library and for daily log with --overrides
# 3. simplify food prompt
# 4. spacing on output

# Assume which date ( Today ) that the food is for, but ask if user wants to change it

#7. type-ahead search for foods







