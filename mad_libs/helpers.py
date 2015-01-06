import sys
import csv

import nltk.data
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

from collections import Counter

def load_POS_tags():
	"""
	Load part of speech tags and descriptions into dictionary data structure
	"""	
	pos_file = "mad_libs/static/tags_to_replace.csv"
	try:
		with open(pos_file, "r") as f:
			pos_tags = {}
			reader = csv.reader(f)
			for row in reader:
				pos_tags[row[0]] = row[1]
		return pos_tags
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)

def load_contractions():
	"""
	Load list of contractions into dictionary data structure
	"""	
	contractions_file = "mad_libs/static/contractions.csv"
	try:
		with open(contractions_file, "rU") as f:
			contractions = {}
			reader = csv.reader(f)
			for row in reader:
				word = row[0]
				# Lowercase
				contractions[word] = ' '.join(word_tokenize(word))
				# First letter capitalized
				word = word[0].upper() + word[1:]
				contractions[word] = ' '.join(word_tokenize(word))
				# Uppercase
				contractions[word.upper()] = ' '.join(word_tokenize(word.upper()))

		return contractions
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)

def single_to_double_quotes(string):
	"""
	Replace single quotes with double quotes
	"""
	# Replace single quotes (not in contractions or apostrophes) with double quotes
	# This will make it easier to rejoin text later
	
	# Turn something like 'The Catcher in the Rye' into "The Catcher in the Rye"
	string = string.replace("' ", "\" ")
	string = string.replace(" '", " \"")

	# Replace `` with "
	string = string.replace("`` ", "\" ")
	string = string.replace(" ``", " \"")
	# Replace '' with "
	string = string.replace("\'\' ", "\" ")
	string = string.replace(" \'\'", " \"")
	
	return string

def tokenize_text(content):
	"""
	Tokenize story text using python NLTK
	"""
	content = single_to_double_quotes(content)
	return pos_tag(word_tokenize(content))

def words_to_replace(raw_text, n):
	"""
	Generate list of n words to replace in raw_text
	"""
	POS_tags = load_POS_tags()

	verbs_to_be = ["is", "am", "are", "was", "were", "been"]

	# Find n most frequent words in the story text
	# Filter for the parts of speech that interest us (contained in pos_tags, not a verb to be)
	most_frequent = Counter(filter(lambda x: (x[0] not in verbs_to_be and x[1] in POS_tags), raw_text)).most_common(n)

	# Pass the template the list of 5 words to replace
	# Save 1) the original word 2) the POS label to replace correctly later and 3) the POS description for the input form
	to_replace = []
	
	for entry in most_frequent:
		word = entry[0][0]
		POS_tag = entry[0][1]
		POS_desc = POS_tags[POS_tag]
		word_tuple = (word, POS_tag, POS_desc)
		to_replace.append(word_tuple)

	return to_replace

def process_user_input(f):
	"""
	Process user input from replacement form
	Put into more usable tuple for display template
	"""
	replacement = []

	# Create a list of tuples to help us find and replace words
	# We need to hold onto the POS tags because some words could be used as different parts of speech
	# This is a bit unlikley with the kinds of words we are replacing (mostly nouns, verbs, adjectives, adverbs) but just to be safe
	for i in range(0,len(f.getlist('raw_word'))):
		if f.getlist('raw_word')[i].istitle():
			# Make sure proper nouns get capitalized
			replacement.append((f.getlist('raw_word')[i], f.getlist('pos_tag')[i], f.getlist('new_word')[i].title()))
		else:
			replacement.append((f.getlist('raw_word')[i], f.getlist('pos_tag')[i], f.getlist('new_word')[i]))

	return replacement

def replace_words(raw_text, replacement):
	"""
	Replace certain words in the raw_text with new mad libs words
	Replace as specified in replacement array of tuples
	"""
	# initialize new text
	new_text = [word for word in raw_text]

	for index, word_tuple in enumerate(raw_text):
		for new_word in replacement:
			if (word_tuple[0] == new_word[0] and word_tuple[1] == new_word[1]):
				# highlight the replaced words in the text using HTML
				new_text[index] = ("<span class=\"-replaced-\">" + new_word[2] + "</span>", new_word[1])
	
	return join_word_tokenized_text(new_text)
	
def join_word_tokenized_text(tokenized_string):
	"""
	Re-construct a string that has been word_tokenized using the nltk function
	"""
	# Join words back together
	tokenized_string = ' '.join(word[0] for word in tokenized_string)
	
	# Clean up punctuation issues caused by the join inserting spaces before punctuation
	# 4 key issues:
	# 1) Space before punctuation at end of clause: "I joined the text , but ..."
	# 2) Space before punctuation at end of sentence: "It doesn't look right ."
	punct_list = [
				 (" ,", ","),
				 (" ;", ";"),
				 (" :", ":"),
				 (" .", "."),
				 (" ?", "?"),
				 (" !", "!")
				 ]
	
	for punct in punct_list:
		tokenized_string = tokenized_string.replace(punct[0], punct[1])

	# 3) Space before apostrophe in contractions: "It 's still not right."
	for key, value in load_contractions().iteritems():
		tokenized_string = tokenized_string.replace(key, value)

	# 4) Remove spaces between before apostrophe s: "Shannon 's"
	tokenized_string = tokenized_string.replace(" \'s", "\'s")

	# 5) Convert single to double quotes
	tokenized_string = single_to_double_quotes(tokenized_string)

	# 6) Remove spaces between quotation marks and quoted text: "She thought, ' geez, that's annoying '."
	quote_count = 0
	to_remove = []
	for index, char in enumerate(tokenized_string):
		if char == "\"":
			# If it's a contraction, pass
			if ((index < len(tokenized_string) - 2 and tokenized_string[index + 1] != " ") and tokenized_string[index - 1] != " "):
				pass
			# If it's a possessive 's, pass
			if (index < len(tokenized_string) - 2 and tokenized_string[index + 1] == "s"):
				pass
			# If it's a quotation mark, fix the spaces
			else:
				quote_count += 1
				# If it's an end quote
				if quote_count % 2 == 0:
					# Remove the space before
					to_remove.append(index - 1)
				# If it's an opening quote
				else:
					# Remove the space after
					to_remove.append(index + 1)
	
	for i in range(0,len(to_remove)):
		tokenized_string = tokenized_string[0:to_remove[i]] + tokenized_string[to_remove[i] + 1:len(tokenized_string)]
		to_remove = [index - 1 for index in to_remove]

	return tokenized_string