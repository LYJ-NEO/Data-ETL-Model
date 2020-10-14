from flask import Blueprint
from flask import request
from flask import make_response, jsonify
from utils.responses import response_with
from utils import responses as resp
from models.authors import Authors,AuthorsSchema
from flask_jwt_extended import jwt_required
from utils.db import db

author_routes = Blueprint("author_routes", __name__)
		
@author_routes.route('/', methods=['GET'])
@jwt_required
def get_author_list():
    fetched = Authors.query.all()
    author_schema = AuthorsSchema(many=True, only=['first_name', 'last_name', 'id'])
    authors, error = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"authors": authors})

@author_routes.route('/<int:author_id>', methods=['GET'])
@jwt_required
def get_author_detail(author_id):
    fetched = Authors.query.get_or_404(author_id)
    author_schema = AuthorSchema()
    author, error = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"author": author})

@author_routes.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_author_detail(id):
    data = request.get_json()
    get_author = Authors.query.get_or_404(id)
    get_author.first_name = data['first_name']
    get_author.last_name = data['last_name']
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorsSchema()
    author, error = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200, value={"author": author})

@author_routes.route('/<int:id>', methods=['PATCH'])
@jwt_required
def modify_author_detail(id):
    data = request.get_json()
    get_author = Authors.query.get(id)
    if data.get('first_name'):
        get_author.first_name = data['first_name']
    if data.get('last_name'):
        get_author.last_name = data['last_name']
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorsSchema()
    author, error = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200, value={"author": author})

@author_routes.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_author(id):
    get_author = Authors.query.get_or_404(id)
    db.session.delete(get_author)
    db.session.commit()
    return response_with(resp.SUCCESS_204)

@author_routes.route('/', methods = ['POST'])
@jwt_required
def create_author():
	try:
		#db.execSQL("PRAGMA foreign_keys=ON")
		data = request.get_json()
		author_schema = AuthorsSchema()
		author = author_schema.load(data)
		result = author_schema.dump(author.data.create())    ##这里作为一个修改点，可能是新版本的的接口调整了
		return response_with(resp.SUCCESS_201, value={"author": result})
	except Exception as e:
		return response_with(resp.INVALID_INPUT_422)