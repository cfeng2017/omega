# -*- coding: utf-8 -*-
import json
import datetime
from apps import db


class MonitorTemplate(db.Model):
    __tablename__ = 't_monitor_template'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='', doc='模板名')
    type = db.Column(db.Integer, nullable=False, default=0, doc='模板对象的类型，0: None, 1: 组， 2:主机， 3:mysql')
    ds_name = db.Column(db.String(50), nullable=False, default='', doc='数据源名')
    ds_description = db.Column(db.String(200), nullable=False, default='', doc='数据源说明')
    chart_name = db.Column(db.String(50), nullable=False, default='', doc='图表名称')
    chart_description = db.Column(db.String(200), nullable=False, default='', doc='图表说明')
    status = db.Column(db.Boolean, nullable=False, default=0, doc='是否开启报警，关闭：0，开启：1')
    rules = db.Column(db.String(1000), nullable=False, default='', doc='报警规则')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, name='', cn='', cd='', dn='', dd='', ar='', ast=1, t=0):
        self.name = name
        self.ds_name = dn
        self.ds_description = dd
        self.chart_name = cn
        self.chart_description = cd
        self.rules = ar
        self.status = ast
        self.type = t

    def __repr__(self):
        return "<MonitorTemplate(name={}, chart_name={}, ds_name={})>".format(self.name, self.chart_name, self.ds_name)

