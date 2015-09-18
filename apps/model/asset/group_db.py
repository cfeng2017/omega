#! -*- coding: utf-8 -*-

from apps import db


class GroupDb(db.Model):
    __tablename__ = 't_group_db'

    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.Integer, nullable=False, default=0, doc='group id')
    db = db.Column(db.String(30), nullable=False, default='', doc='组名')

    def __init__(cls, gid, db_name):
        cls.gid = gid
        cls.db = db_name

    def __repr__(cls):
        return "<GroupType(id={}, db={})>".format(cls.id, cls.db)

db.Index('idex_gid', GroupDb.gid)
db.Index('idex_db', GroupDb.db)
