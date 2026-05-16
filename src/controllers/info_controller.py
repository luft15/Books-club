from flask import render_template
from app import app


@app.route("/info")
def information():
    return render_template("information.html")
