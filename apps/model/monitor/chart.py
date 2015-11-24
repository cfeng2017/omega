# -*- coding: utf-8 -*-
from apps import db


class Chart(db.Model):
    __tablename__ = 't_monitor_chart'

    id = db.Column(db.Integer, primary_key=True)
    chart_name = db.Column(db.String(50), nullable=False, default='', doc='图表名称')
    gid = db.Column(db.Integer, nullable=False, default=0, doc='组id')
    hid = db.Column(db.Integer, nullable=False, default=0, doc='host id')
    iid = db.Column(db.Integer, nullable=False, default=0, doc='实例id')
    creator = db.Column(db.Integer, nullable=False, default=0, doc='建表用户id')
    receiver = db.Column(db.String(200), nullable=False, default='', doc='接警人id，多个联系人以空格分隔')
    alarm_status = db.Column(db.Boolean, nullable=False, default=0, doc='是否开启报警，关闭：0，开启：1')
    create_time = db.Column(db.DateTime, nullauble=False, default='', doc='建图日期')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, dn, cn, gid, hid, iid, creator, contacts, alarm_status, mtid):
        self.ds_name = dn
        self.chart_name = cn
        self.gid = gid
        self.hid = hid
        self.iid = iid
        self.creator = creator
        self.contacts = contacts
        self.alarm_status = alarm_status
        self.monitor_template_id = mtid

    def __repr__(self):
        return "<Chart(id={}, gid={}, hid={}, iid={})>".format(self.id, self.gid, self.hid, self.iid)


db.Index('idx_gid', Chart.gid)
db.Index('idx_hid', Chart.hid)
db.Index('idx_iid', Chart.iid)
db.Index('idx_tmid', Chart.monitor_template_id)

