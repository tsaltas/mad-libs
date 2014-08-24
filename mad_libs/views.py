from flask import render_template, request, redirect, url_for

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.probability import FreqDist
import nltk.data

from collections import Counter

import csv

from mad_libs import app

@app.route("/", methods=["GET"])
def input_form():
	# Get part of speech tags and descriptions into dictionary (only ones we want users to replace)
	pos_file = "mad_libs/static/tags_to_replace.csv"
	with open(pos_file, "r") as f1:
		pos_tags = {}
		reader = csv.reader(f1)
		for row in reader:
			pos_tags[row[0]] = row[1]

	# Get raw story text
	story_file = "mad_libs/static/story.txt"
	with open(story_file, "r") as f2:
		story_text = f2.read()
	labelled_text = pos_tag(word_tokenize(story_text))

	# find 5 most frequent words in the story text, filtering for the parts of speech that interest us
	most_frequent = Counter(filter(lambda x: x[1] in pos_tags, labelled_text)).most_common(5)

	# pass the template the list of 5 words to replace, include parts of speech for when we actually do the replacement
	to_replace = []
	for entry in most_frequent:
		word = entry[0][0]
		tag = entry[0][1]
		desc = pos_tags[tag]
		new_tuple = (word, tag, desc)
		to_replace.append(new_tuple)

	return render_template("input_form.html", to_replace=to_replace)

@app.route("/", methods=["POST"])
def display_story():
	
	to_replace = []
	f = request.form

	# Create a list of tuples to help us find and replace words
	# We needed to hold onto the POS tags because some words could be used as different parts of speech
	# This is a bit unlikley with the kinds of words we are replacing (mostly nouns, verbs, adjectives, adverbs) but just to be safe
	for i in range(0,len(f.getlist('raw_word'))):
		if f.getlist('raw_word')[i].istitle():
			# Make sure proper nouns get capitalized
			to_replace.append((f.getlist('raw_word')[i], f.getlist('pos_tag')[i], f.getlist('new_word')[i].title()))
		else:
			to_replace.append((f.getlist('raw_word')[i], f.getlist('pos_tag')[i], f.getlist('new_word')[i]))
	
	# Get raw story text
	story_file = "mad_libs/static/story.txt"
	with open(story_file, "r") as f1:
		story_text = f1.read()
	labelled_text = pos_tag(word_tokenize(story_text))

	# Do replacement
	for index, word_tuple in enumerate(labelled_text):
		for new_word in to_replace:
			if (word_tuple[0] == new_word[0] and word_tuple[1] == new_word[1]):
				labelled_text[index] = (new_word[2], new_word[1])

	# Join words together and clean up punctuation issues
	new_text = ' '.join(word[0] for word in labelled_text)
	# Remove space before punctuation at end of clause
	new_text = new_text.replace(" ,", ",")
	new_text = new_text.replace(" ;", ";")
	new_text = new_text.replace(" :", ":")
	# Remove space before punctuation at end of sentence 
	new_text = new_text.replace(" .", ".")
	new_text = new_text.replace(" ?", "?")
	new_text = new_text.replace(" !", "!")
	# Remove space before apostrophe in contractions
	contractions_file = "mad_libs/static/contractions.csv"
	with open(contractions_file, "rU") as f2:
		contractions = {}
		reader = csv.reader(f2)
		for row in reader:
			contractions[row[1]] = row[0]
	for key in contractions:
		new_text = new_text.replace(key, contractions[key])
	# Remove spaces between quotation marks and quoted text
	new_text = new_text.replace("``", "\"")
	new_text = new_text.replace("\'\'", "\"")
	new_text = new_text.replace(" \'s", "\'s")

	quote_count = 0
	to_remove = []
	for index, char in enumerate(new_text):
		if (char == "\"" or char == "\'"):
			# If it's a contraction, pass
			if ((index < len(new_text) - 2 and new_text[index + 1] != " ") and new_text[index - 1] != " "):
				pass
			# If it's a possessive 's, pass
			if (index < len(new_text) - 2 and new_text[index + 1] == "s"):
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
		new_text = new_text[0:to_remove[i]] + new_text[to_remove[i] + 1:len(new_text)]
		to_remove = [x - 1 for x in to_remove]

	return render_template("display_story.html", story=new_text)