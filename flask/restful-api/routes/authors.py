#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from utils.responses import response_with
from utils import responses as resp
from models.authors import Author,AuthorSchmea
from utils.database import db

author_routes = Blueprint("author_routes", __name__)

@author_routes.route('/', methods=['POST'])
def create_author():
	try:
		data = request.get_json()
		author_schema = AuthorSchmea()
		author = author_schema.load(data)
		result = author_schema.dump(author.create()).data
		return response_with(resp.SUCCESS_201, value={"author":result})
	except Exception as e:
		print(e)
		return response_with(resp.INVALID_INPUT_422)