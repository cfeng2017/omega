# -*- coding: utf8 -*-
from apps import db


class MysqlInstance(db.Model):
    __tablename__ = 't_mysql_instance'

    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.Integer, nullable=False, doc='组id')
    hid = db.Column(db.Integer, nullable=False, doc='主机id')
    ip = db.Column(db.String(256), nullable=False, doc='ip')
    port = db.Column(db.Integer, nullable=False, default=3306, doc='端口号')
    version = db.Column(db.String(20), nullable=False, doc='版本号')
    role = db.Column(db.Integer, nullable=False, default=0, doc='角色，master:1, slave: 2')
    status = db.Column(db.Integer, nullable=False, default=0, doc='状态。online:1, offline: 2')
    remark = db.Column(db.String(200), nullable=False, default='', doc='备注，如机器用做backup或etl等')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, gid, hid, ip, port, role, status, version='', remark=''):
        self.gid = gid
        self.hid = hid
        self.ip = ip
        self.port = port
        self.version = version
        self.role = role
        self.status = status
        self.remark = remark

    def __repr__(self):
        return "<MysqlInstance(id={}, gid={}, hid={}, port={})>".format(self.id, self.gid, self.hid, self.port)

db.Index('idx_gid_hid', MysqlInstance.gid, MysqlInstance.hid)
db.Index('idx_ip', MysqlInstance.ip)

