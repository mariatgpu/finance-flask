from flask import Flask
from src.stock.route import stock_blueprint

def init_app(app: Flask):
    app.register_blueprint(stock_blueprint)
