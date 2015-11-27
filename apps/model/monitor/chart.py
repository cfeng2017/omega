# -*- coding: utf-8 -*-
from apps import db


class Chart(db.Model):
    __tablename__ = 't_monitor_chart'

    id = db.Column(db.Integer, primary_key=True)
    template_name_id = db.Column(db.Integer, nullable=False, default=0, doc='t_monitor_template_name的id')
    name = db.Column(db.String(50), nullable=False, default='', doc='图表名称')
    description = db.Column(db.String(500), nullable=False, default='', doc='图表描述')
    gid = db.Column(db.Integer, nullable=False, default=0, doc='组id')
    hid = db.Column(db.Integer, nullable=False, default=0, doc='host id')
    iid = db.Column(db.Integer, nullable=False, default=0, doc='实例id')
    creator = db.Column(db.Integer, nullable=False, default=0, doc='建表用户id')
    receiver = db.Column(db.String(200), nullable=False, default='', doc='接警人id，多个联系人以空格分隔')
    create_time = db.Column(db.DateTime, nullable=False, default='0000-00-00 00:00:00', doc='建图日期')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, tid=0, cn='', cd='', gid=0, hid=0, iid=0, creator=0, receiver='', ct=''):
        self.template_name_id = tid
        self.name = cn
        self.description = cd
        self.gid = gid
        self.hid = hid
        self.iid = iid
        self.creator = creator
        self.receiver = receiver
        self.create_time = ct

    def __repr__(self):
        return "<Chart(id={}, name={}, description={})>".format(self.id, self.name, self.description)


db.Index('idx_tid', Chart.template_name_id)
db.Index('idx_gid', Chart.gid, Chart.iid)
db.Index('idx_hid', Chart.hid)

