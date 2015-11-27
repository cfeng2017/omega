# -*- coding: utf-8 -*-
from apps import db


class Ds(db.Model):
    __tablename__ = 't_monitor_ds'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='', doc='数据源名称')
    description = db.Column(db.String(500), nullable=False, default='', doc='数据源描述')
    chart_id = db.Column(db.Integer, nullable=False, default=0, doc='t_monitor_chart的id')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, name='', desc='', cid=0):
        self.name = name
        self.description = desc
        self.chart_id = cid

    def __repr__(self):
        return "<Ds(id={}, name={}, chart_id={})>".format(self.id, self.name, self.chart_id)

db.Index('idx_cid', Ds.chart_id)



