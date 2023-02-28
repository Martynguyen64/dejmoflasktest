import threading

# import "packages" from flask
from flask import (
    render_template,
)  # import render_template from "public" flask libraries

# import "packages" from "this" project
from __init__ import app, db  # Definitions initialization

from model.users import initUsers
from model.fitness import init_diets

# from model.fitness import initUsers
from api.user import user_api  # Blueprint import api definition
from api.fitness import diets_bp

app.register_blueprint(user_api)  # register api routes
app.register_blueprint(diets_bp)  # register api routes


@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404


@app.route("/")  # connects default URL to index() function
def index():
    return render_template("index.html")


@app.route("/stub/")  # connects /stub/ URL to stub() function
def stub():
    return render_template("stub.html")


@app.before_first_request
def activate_job():
    with app.app_context():
        db.create_all()
        print("test")
        initUsers()
        initUsers()
        init_diets()


# this runs the application on the development server
if __name__ == "__main__":
    db.init_app(app)
    # change name for testing
    from flask_cors import CORS

    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port="8086")

