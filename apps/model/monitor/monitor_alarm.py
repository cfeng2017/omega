# -*- coding: utf-8 -*-
from apps import db


class MonitorAlarm(db.Model):
    __tablename__ = 't_monitor_alarm'

    id = db.Column(db.Integer, primary_key=True)
    template_name_id = db.Column(db.Integer, nullable=False, default=0, doc='monitor_tempalte_name的id')
    template_id = db.Column(db.Integer, nullable=False, default=0, doc='moitor_tempalte的id')
    mode = db.Column(db.TINYINT, nullable=False, default=0, doc='报警模式。1: 上限，2: 下限，3: 范围，4: 斜率')
    warn_lower = db.Column(db.Integer, nullable=False, default=0, doc='警告下限值')
    warn_upper = db.Column(db.Integer, nullable=False, default=0, doc='警告上限值')
    disaster_lower = db.Column(db.Integer, nullable=False, default=0, doc='灾难下限值')
    disaster_upper = db.Column(db.Integer, nullable=False, default=0, doc='灾难上限值')
    last = db.Column(db.Integer, nullable=False, default=0, doc='持续时间')
    interval = db.Column(db.Integer, nullable=False, default=0, doc='间隔时间')
    begin_time = db.Column(db.DateTime, nullable=False, default='1000-01-01 00:00:00', doc='起始时间')
    end_time = db.Column(db.DateTime, nullable=False, default='1000-01-01 00:00:00', doc='终止时间')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, tnid, tid, mode, wl, wu, dl, du, last, interval, bt, et):
        self.template_name_id = tnid
        self.template_id = tid
        self.mode = mode
        self.warn_lower = wl
        self.warn_upper = wu
        self.disaster_lower = dl
        self.disaster_upper = du
        self.last = last
        self.interval = interval
        self.begin_time = bt
        self.end_time = et

    def __repr__(self):
        return "<MonitorAlarm(id={}, template_name_id={}, template_id={})>".\
            format(self.id, self.template_name_id, self.template_id)

db.Index('idx_tnid', MonitorAlarm.template_name_id)
db.Index('idx_tid', MonitorAlarm.template_id)


