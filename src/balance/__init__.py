from flask import Flask
from src.balance.route import balance_blueprint

def init_app(app: Flask):
    app.register_blueprint(balance_blueprint)
