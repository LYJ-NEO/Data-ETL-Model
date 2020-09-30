#!/usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------
#  构建ORM对象：从 SQLAchemy的Model继承
#  构建Schema对象：从marshmallow的ModelSchema继承
#-----------------------------------------------------------------

from utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class Book(db.Model):

    __tablename__ = 'books'     # 定义表名
    id = db.Column(db.Integer, primary_key = True )    # 自增长主键
    title = db.Column(db.String(50))        # Book Title
    year  = db.Column(db.Integer) 
    author_id = db.Column( db.Integer , db.ForeignKey('authors.id') , nullable = False)

    def __init__(self , title , year , author_id = None):
        self.title = title 
        self.year  = year 
        self.author_id = author_id 

    def create(self):           # 向数据库中写入本对象数据
        db.session.add(self)
        db.session.commit()
        return self

class BookSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Book 
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    year = fields.Integer(required=True)
    author_id = fields.Integer()


