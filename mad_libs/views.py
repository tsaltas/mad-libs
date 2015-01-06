from flask import render_template, request, redirect, url_for

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
	return render_template("new_story.html")

@app.route("/new_story", methods=["POST"])
def new_story_post():
	story = Story(
		title=request.form["title"],
		author = request.form["author"],
		content=request.form["content"]
	)
	session.add(story)
	session.commit()
	# Redirect user to form to fill in words
	return redirect(url_for('input_form', story_id = story.id))

# ----User can play mad libs---- #

@app.route("/mad_libs/<story_id>", methods=["GET"])
def input_form(story_id):
	story = session.query(Story).get(story_id)
	raw_text = tokenize_text(story.content)

	# Find 5 most common words to replace and send to the input form template
	return render_template("input_form.html", to_replace=words_to_replace(raw_text, len(raw_text)/20), title=story.title)

@app.route("/mad_libs/<story_id>", methods=["POST"])
def display_story(story_id):
	story = session.query(Story).get(story_id)
	raw_text = tokenize_text(story.content)

	# Turn request form data into more useful list of tuples
	replacement = process_user_input(request.form)

	return render_template("display_story.html",
		story=replace_words(raw_text, replacement),
		title=story.title,
		author=story.author,
		date=story.datetime
	)

# ----About page---- #

@app.route("/about")
def about():
	return render_template("about.html")

# ----Error Handling---- #
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500