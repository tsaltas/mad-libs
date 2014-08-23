from flask import render_template, request, redirect, url_for

from mad_libs import app


@app.route("/", methods=["GET"])
def input_form():
	input_list = [('1','noun'), ('4','adjective')]
	return render_template("input_form.html", inputs=input_list)

@app.route("/", methods=["POST"])
def display_story():
	filename = "mad_libs/static/story.txt"

	with open(filename, "r") as f:
		story_text = f.read().strip()
	
	story_text = story_text.strip()
	story_text = story_text.split()
	story_text[1] = request.form["1"]
	story_text[4] = request.form["4"]
	story_text = ' '.join(story_text)
	story_text = story_text + '.'
	
	return render_template("display_story.html", story=story_text)