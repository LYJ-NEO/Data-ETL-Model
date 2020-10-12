from utils.db import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from models.books import BookSchema

class Authors(db.Model):
	__tablename__ = 'authors'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	first_name = db.Column(db.String(20))
	last_name = db.Column(db.String(20))
	created = db.Column(db.DateTime, server_default=db.func.now())
	books = db.relationship('Book', backref='Authors', cascade="all, delete-orphan")

	def __init__(self, first_name, last_name, books=[]):
		self.first_name = first_name
		self.last_name = last_name
		self.books = books

	def create(self):
		db.session.add(self)
		db.session.commit()
		return self	
		
class AuthorsSchema(ModelSchema):			   #使用marshmallow中的模型说明
	class Meta(ModelSchema.Meta):
		model = Authors
		sqla_session = db.session

	id = fields.Number(dump_only=True)
	first_name = fields.String(required=True)
	last_name = fields.String(required=True)
	created = fields.String(dump_only=True)
	books = fields.Nested(BookSchema, many=True, only=['title','year','id'])	