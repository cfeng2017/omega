#! -*- coding: utf-8 -*-
from apps import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False, default='')
    email = db.Column(db.String(120), nullable=False, default='')
    mobile = db.Column(db.String(65), nullable=False, default='')
    english_name = db.Column(db.String(50), nullable=False, default='')
    department_name = db.Column(db.String(30), nullable=False, default='')
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_alive = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, uid, name, email, mobile, english_name, department_name, is_admin, is_alive):
        self.uid = uid
        self.name = name
        self.email = email
        self.mobile = mobile
        self.english_name = english_name
        self.department_name = department_name
        self.is_admin = is_admin
        self.is_alive = is_alive

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User {}>'.format(self.name)
