from flask import Flask

# from db.db import connect_db


app = Flask(__name__)

# db_con = connect_db()

from controllers.index_controller import *
from controllers.info_controller import *
from controllers.plan_controller import *

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=80,
        debug=True
    )