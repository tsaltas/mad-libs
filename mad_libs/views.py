from flask import render_template, request
from mad_libs import app

from helpers import *

# load raw story texts with POS labels outside main routes to save time
raw_text = load_raw_text()

# ----Home page---- #

@app.route("/")
def story_list():
	pass

@app.route("/new_story", methods=["GET"])
def new_story_get():
	# Get new story from user
	pass

# ----User can create new stories---- #

@app.route("/new_story", methods=["POST"])
def new_story_post():
	# Redirect user to form to fill in words
	pass

# ----User can play mad libs---- #

@app.route("/mad_libs", methods=["GET"])
def input_form():
	
	# Get appropriate story text

	# Find 5 most common words to replace and send to the input form template
	return render_template("input_form.html", to_replace=words_to_replace(raw_text, 5))

@app.route("/mad_libs", methods=["POST"])
def display_story():
	
	# Turn request form data into helpful list of tuples
	replacement = process_user_input(request.form)
	
	# Get appropriate story text

	# Do replacement and send to the story display template
	return render_template("display_story.html", story=replace_words(raw_text, replacement))

# ----About page---- #

@app.route("/about")
def about():
	return render_template("about.html")