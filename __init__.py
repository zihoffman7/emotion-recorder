from flask import Flask
import main

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.secret_key = "tan the man"
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.register_blueprint(main.main)
    return app
