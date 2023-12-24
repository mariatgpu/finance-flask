from flask import Flask
from src.middlewares.ensure_no_cache import ensure_no_cache
from src.middlewares.exception_handler import handle_error

def init_app(app: Flask):
    app.after_request(ensure_no_cache)
    app.register_error_handler(Exception, handle_error)
