# -*- coding: utf-8 -*-

from apps import db


class GroupDb(db.Model):
    __tablename__ = 't_group_db'

    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.Integer, nullable=False, default=0, doc='group id')
    db = db.Column(db.String(30), nullable=False, default='', doc='组名')

    def __init__(self, gid, db_name):
        self.gid = gid
        self.db = db_name

    def __repr__(self):
        return "<GroupType(id={}, db={})>".format(self.id, self.db)

db.Index('idex_gid', GroupDb.gid)
db.Index('idex_db', GroupDb.db)
