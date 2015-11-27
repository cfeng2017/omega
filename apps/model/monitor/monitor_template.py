# -*- coding: utf-8 -*-
from sqlalchemy.dialects.mysql import TINYINT, TIME

from apps import db


class MonitorTemplate(db.Model):
    __tablename__ = 't_monitor_template'

    id = db.Column(db.Integer, primary_key=True)
    template_name_id = db.Column(db.String(50), nullable=False, default='', doc='模板名id')
    chart_name = db.Column(db.String(50), nullable=False, default='', doc='图表名称')
    chart_description = db.Column(db.String(200), nullable=False, default='', doc='图表说明')
    ds_name = db.Column(db.String(50), nullable=False, default='', doc='数据源名')
    ds_description = db.Column(db.String(200), nullable=False, default='', doc='数据源说明')
    status = db.Column(db.Boolean, nullable=False, default=0, doc='是否开启报警，关闭：0，开启：1')
    mode = db.Column(TINYINT, nullable=False, default=0, doc='报警模式。1: 上限，2: 下限，3: 范围，4: 斜率')
    warn_lower = db.Column(db.Integer, nullable=False, default=0, doc='警告下限值')
    warn_upper = db.Column(db.Integer, nullable=False, default=0, doc='警告上限值')
    disaster_lower = db.Column(db.Integer, nullable=False, default=0, doc='灾难下限值')
    disaster_upper = db.Column(db.Integer, nullable=False, default=0, doc='灾难上限值')
    last = db.Column(db.Integer, nullable=False, default=0, doc='持续时间')
    interval = db.Column(db.Integer, nullable=False, default=0, doc='间隔时间')
    begin_time = db.Column(TIME, nullable=False, default='00:00', doc='起始时间')
    end_time = db.Column(TIME, nullable=False, default='00:00', doc='终止时间')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, tnid=0, cn='', cd='', dn='', dd='', status=0, mode=0,
                 wl=0, wu=0, dl=0, du=0, last=0, inter=0, bt='00:00', et='00:00'):
        self.template_name_id = tnid
        self.chart_name = cn
        self.chart_description = cd
        self.ds_name = dn
        self.ds_description = dd
        self.status = status
        self.mode = mode
        self.warn_lower = wl
        self.warn_upper = wu
        self.disaster_lower = dl
        self.disaster_upper = du
        self.last = last
        self.interval = inter
        self.begin_time = bt
        self.end_time = et

    def __repr__(self):
        return "<MonitorTemplate(template_name_id={}, chart_name={}, ds_name={})>".format(self.template_name_id,
                                                                                          self.chart_name, self.ds_name)

db.Index('idx_1', MonitorTemplate.template_name_id, MonitorTemplate.chart_name, MonitorTemplate.ds_name)