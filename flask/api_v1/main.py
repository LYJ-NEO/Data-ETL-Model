from flask import Flask
from flask import jsonify
from utils.db import db
from utils.responses import response_with
import utils.responses as resp
from routes.authors import author_routes
from routes.books import book_routes
from config.config import DevelopmentConfig, ProductionConfig, TestingConfig
import os
import logging

app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)

db.init_app(app)						# 延迟绑定，创建
with app.app_context():
    db.create_all()
	
app.register_blueprint(author_routes, url_prefix='/api/authors/')
app.register_blueprint(book_routes, url_prefix='/api/books/')
	
@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)

@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)

db.init_app(app)
with app.app_context():
    # from api.models import *
    db.create_all()
	
if __name__ == "__main__":
    app.run(debug=True)	
