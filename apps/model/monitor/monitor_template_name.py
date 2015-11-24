# -*- coding: utf-8 -*-
from apps import db


class MonitorTemplateName(db.Model):
    __tablename__ = 't_monitor_template_name'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='', doc='监控模板名')
    monitor_type = db.Column(db.String(50), nullable=False, default='', doc='模板对象的类型')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, ty='', name=''):
        self.monitor_type = ty
        self.name = name

    def __repr__(self):
        return "<MonitorTemplateName(id={}, name={}, monitor_type={})>".format(self.id, self.name, self.monitor_type)


