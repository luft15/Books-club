from flask import Flask
from dependencies import AppModule
from flask_injector import FlaskInjector

app = Flask(__name__)

from controllers.index_controller import *
from controllers.info_controller import *
from controllers.plan_controller import *

Flask.url_for.__annotations__ = {}  # нужно, чтобы Flask не оборачивал url_for в представлениях
FlaskInjector(app=app, modules=[AppModule()])

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=80,
        debug=True
    )