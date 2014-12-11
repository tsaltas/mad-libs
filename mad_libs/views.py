from flask import render_template, request

from mad_libs import app
from database import session
from models import Story

from helpers import *

# ----Home page---- #

@app.route("/")
def stories():
	stories = session.query(Story)
	stories = stories.order_by(Story.datetime.desc())
	stories = stories.all()
	return render_template("stories.html", stories=stories)

# ----User can create new stories---- #

@app.route("/new_story", methods=["GET"])
def new_story_get():
	# Get new story from user
	pass

@app.route("/new_story", methods=["POST"])
def new_story_post():
	# Redirect user to form to fill in words
	pass

# ----User can play mad libs---- #

@app.route("/mad_libs/<story_id>", methods=["GET"])
def input_form(story_id):
	story = session.query(Story).get(story_id)
	raw_text = tokenize_text(story.content)

	# Find 5 most common words to replace and send to the input form template
	return render_template("input_form.html", to_replace=words_to_replace(raw_text, 5))

@app.route("/mad_libs/<story_id>", methods=["POST"])
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