from flask import render_template

from mad_libs import app

@app.route("/")
def index():
    return render_template("index.html")