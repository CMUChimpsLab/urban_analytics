#!/usr/bin/python
import re, string

class ParseTweet(): 

	@staticmethod
	def get_one_number(str):
		words_split = string.split(str)
		words_split = [word.strip(string.punctuation) for word in words_split]
		numbers = words_to_numbers(words_split)
		numbers = combine_two_numbers_next_to_each_other(numbers)
		numbers = remove_negative_numbers(numbers)
		count = len(numbers) # number of zero or positive numbers.

		if (count == 1): return round(float(numbers[0]), 1)
		if (count == 2): return round(((numbers[0] + numbers[1]) / 2.0), 1)
		if (len(str) > 1 and count  == 0 or count > 2): 
			return -1.0

	@staticmethod
	def get_one_letter(str): # for multiple choice
	# Gets first single lettered word from given string, ignores 'i'
		words_split = string.split(str)
		words_split = [word.strip(string.punctuation) for word in words_split]
		for word in words_split:
			word = word.lower()
			if len(word) == 1 and word != 'i':
				return word.lower()
		return 'None' # No single letter word found. 

	@staticmethod
	def check_for_missing_space(str):
	# Adds one space in between each character and tries getting
	# one integer from modified string
		length = len(str)
		for i in xrange(length):
			modified_str = str[:i] + ' ' + str[i:] 
			parsed = ParseTweet.get_one_number(modified_str)
			if parsed != -1:
				return parsed
		return -1.0

def words_to_numbers(array_of_str):    
	array_of_numbers = []   
	for str in array_of_str:
		converted = word_to_number(str)
		array_of_numbers.append(converted)
	return array_of_numbers

def word_to_number(str):
	str = str.lower()
	if len(str) == 0: return -1
	if str in ["none", "any"]: return 0
	try:     
		number = float(str)
	except:     
		try: number = spoken_word_to_number(str)
		except: number = -1.0 
	return number 

def combine_two_numbers_next_to_each_other(array_of_numbers):
	# [3, 40, 2, -1, 20, 22] -> [3, 42, -1, 20, 22] 
	new_array = []
	number_count = len(array_of_numbers)
	i = 0 
	while (i < number_count):
		number = array_of_numbers[i]
		if (number != -1 and number % 10 == 0
			and i + 1 < number_count and array_of_numbers[i + 1] != -1 and
			array_of_numbers[i + 1] < 10):
			combined_number = array_of_numbers[i] + array_of_numbers[i + 1] 
			new_array.append(combined_number) 
			i += 2
		else:
			new_array.append(number)
			i += 1
	return new_array

def remove_negative_numbers(array_of_numbers):
	new_array = []
	for n in array_of_numbers:
		if n >= 0:
			new_array.append(n)
	return new_array

# spoken_word_to_number from
# http://code.activestate.com/recipes/578258-spoken-word-to-number/
_known = {
	'zero': 0,
	'one': 1,
	'two': 2,
	'three': 3,
	'four': 4,
	'five': 5,
	'six': 6,
	'seven': 7,
	'eight': 8,
	'nine': 9,
	'ten': 10,
	'eleven': 11,
	'twelve': 12,
	'thirteen': 13,
	'fourteen': 14,
	'fifteen': 15,
	'sixteen': 16,
	'seventeen': 17,
	'eighteen': 18,
	'nineteen': 19,
	'twenty': 20,
	'thirty': 30,
	'forty': 40,
	'fifty': 50,
	'sixty': 60,
	'seventy': 70,
	'eighty': 80,
	'ninety': 90
	}

def spoken_word_to_number(n):
# Assumes n is a positive integer. Returns error if not.
	if len(n) == 0: return None 
	n = n.lower().strip()
	if n in _known:
		return _known[n]
	else:
		inputWordArr = re.split('[ -]', n)

	assert len(inputWordArr) > 1 # all single words are known
	#Check the pathological case where hundred or thousand is at end
	if inputWordArr[-1] == 'hundred':
		inputWordArr.append('zero')
		inputWordArr.append('zero')
	if inputWordArr[-1] == 'thousand':
		inputWordArr.append('zero')
		inputWordArr.append('zero')
		inputWordArr.append('zero')
	if inputWordArr[0] == 'hundred':
		inputWordArr.insert(0, 'one')
	if inputWordArr[0] == 'thousand':
		inputWordArr.insert(0, 'one')

	inputWordArr = [word for word in inputWordArr if word not in ['and', 'minus', 'negative']]
	currentPosition = 'unit'
	prevPosition = None
	output = 0
	for word in reversed(inputWordArr):
		if currentPosition == 'unit':
			number = _known[word]
			output += number
			if number > 9:
				currentPosition = 'hundred'
			else:
				currentPosition = 'ten'
		elif currentPosition == 'ten':
			if word != 'hundred':
				number = _known[word]
				if number < 10:
					output += number*10
				else:
					output += number
			currentPosition = 'hundred'
		elif currentPosition == 'hundred':
			if word not in [ 'hundred', 'thousand']:
				number = _known[word]
				output += number*100
				currentPosition = 'thousand'
			elif word == 'thousand':
				currentPosition = 'thousand'
			else:
				currentPosition = 'hundred'
		elif currentPosition == 'thousand':
			assert word != 'hundred'
			if word != 'thousand':
				number = _known[word]
				output += number*1000
		else:
			assert "Can't be here" == None
	return(output)