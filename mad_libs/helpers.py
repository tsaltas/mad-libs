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

def tokenize_text(content):
	"""
	Tokenize story text using python NLTK
	"""
	return pos_tag(word_tokenize(content))

def words_to_replace(raw_text, n):
	"""
	Generate list of n words to replace in raw_text
	"""
	POS_tags = load_POS_tags()

	verbs_to_be = ["is"
		, "isn't"
		, "he's"
		, "she's"
		, "it's"
		, "am"
		, "I'm"
		, "are"
		, "you're"
		, "they're"
		, "we're"
		, "was"
		, "wasn't"
		, "were"
		, "weren't"
		, "been"
		, "had"
		, "hadn't"
		, "have"
		, "haven't"
		, "has"
		, "hasn't"
		, "will"
		, "won't"
	]

	# Find n most frequent words in the story text
	# Filter for the parts of speech that interest us (contained in POS_tags, not a verb to be)
	most_frequent = Counter(filter(lambda x: (x[0] not in verbs_to_be and x[1] in POS_tags), raw_text)).most_common(n)

	# Pass the template the list of n words to replace
	# Save 1) the original word 2) the POS description for the user input form
	to_replace = []
	
	for entry in most_frequent:
		word = entry[0][0]
		POS_tag = entry[0][1]
		POS_desc = POS_tags[POS_tag]
		word_tuple = (word, POS_desc)
		to_replace.append(word_tuple)

	return to_replace

def process_user_input(f):
	"""
	Process user input from replacement form
	Put into more useful tuple for display template
	"""
	replacement = []

	# Create a list of tuples to help us find and replace words
	for i in range(0,len(f.getlist('raw_word'))):
		if f.getlist('raw_word')[i].istitle():
			# Make sure proper nouns get capitalized
			replacement.append((f.getlist('raw_word')[i], f.getlist('new_word')[i].title()))
		else:
			replacement.append((f.getlist('raw_word')[i], f.getlist('new_word')[i]))

	return replacement

def replace_words(raw_text, replacement):
	"""
	Replace certain words in the raw_text with new mad libs words
	Replace as specified in replacement array of tuples
	"""
	for word_tuple in replacement:
		print "replacing " + word_tuple[0] + " with " + word_tuple[1]
		raw_text = raw_text.replace(word_tuple[0], "<span class=\"replaced\">" + word_tuple[1] + "</span>")

	# Preserve the new lines in the final display
	raw_text = raw_text.replace("\n", "<br>")

	return raw_text