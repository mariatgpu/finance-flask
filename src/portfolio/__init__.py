from flask import Flask
from src.portfolio.route import portfolio_blueprint

def init_app(app: Flask):
    app.register_blueprint(portfolio_blueprint)
