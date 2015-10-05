# -*- coding: utf-8 -*-
from apps import db


class Group(db.Model):
    __tablename__ = 't_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='', doc='组名')
    type = db.Column(db.SmallInteger, nullable=False, default=0, doc='组类型Id')
    description = db.Column(db.String(200), nullable=False, default='', doc='组描述')
    scenario = db.Column(db.String(500), nullable=False, default='', doc='使用场景')
    contacts = db.Column(db.String(100), nullable=False, default='', doc='联系人')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, name='', gtype=0, des='', scenario='', contacts='', updatetime=''):
        self.name = name
        self.type = gtype
        self.description = des
        self.scenario = scenario
        self.contacts = contacts
        self.updatetime = updatetime

    def __repr__(self):
            return "<Group(id={}, name={}, type={})>".format(self.id, self.name, self.type)

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'description': self.description,
            'scenario': self.scenario,
            'contacts': self.contacts
        }