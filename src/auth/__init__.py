from flask import Flask
from src.auth.route import auth_blueprint

def init_app(app: Flask):
    app.register_blueprint(auth_blueprint)
