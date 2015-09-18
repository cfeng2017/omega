#! -*- coding: utf-8 -*-

from apps import db


class GroupType(db.Model):
    __tablename__ = 't_group_type'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False, default='', doc='类型名')

    def __init__(self, gtype):
        self.type = gtype

    def __repr__(self):
        return "<GroupType(id={}, type={})>".format(self.id, self.type)

