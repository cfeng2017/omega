# -*- coding: utf-8 -*-
from apps import db
from sqlalchemy.dialects.mysql import TINYINT, TIME


class MonitorAlarm(db.Model):
    __tablename__ = 't_monitor_alarm'

    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, nullable=False, default=0, doc='t_moitor_template的id')
    ds_id = db.Column(db.Integer, nullable=False, default=0, doc='ds的id')
    status = db.Column(db.Boolean, nullable=False, default=0, doc="是否开启报警")
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

    def __init__(self, tid=0, did=0, status=0, mode=0, wl=0, wu=0, dl=0, du=0, last=0, interval=0, bt='00:00', et='00:00'):
        self.template_id = tid
        self.ds_id = did
        self.status = status
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
        return "<MonitorAlarm(id={}, ds_id={})>".format(self.id, self.ds_id)

db.Index('idx_tid', MonitorAlarm.template_id)
db.Index('idx_dsid', MonitorAlarm.ds_id)


