#! -*- coding: utf-8 -*-

from app import db

class Group(db.Model):
    import datetime
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='', doc='组名')
    type = db.Column(db.SmallInteger, nullable=False, default=0, doc='组类型，如Mysql:1, Memcached:2, '
                                                                     'Redis:3, Hadoop:4, HBase:5')
    description = db.Column(db.String(200), nullable=False, default='', doc='组描述')
    scenario = db.Column(db.String(500), nullable=False, default='', doc='使用场景')
    contacts = db.Column(db.String(100), nullalbe=False, default='', doc='联系人')
    updatetime = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now)



