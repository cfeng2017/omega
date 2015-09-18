#! -*- encoding: utf8 -*-
from apps import db


class RedisInstance(db.Model):
    __tablename__ = 't_redis_instance'

    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.Integer, nullable=False, doc='组id')
    hid = db.Column(db.Integer, nullable=False, doc='主机id')
    ip = db.Column(db.String(256), nullable=False, doc='ip')
    port = db.Column(db.Integer, nullable=False, doc='端口号')
    version = db.Column(db.String(20), nullable=False, doc='版本号')
    memory = db.Column(db.Integer, nullable=False, doc='分配内存，单位MB')
    persistence = db.Column(db.Integer, nullable=False, default=0, doc='是否持久化，否：0，是：1')
    role = db.Column(db.Integer, nullable=False, default=0, doc='角色，master:1, slave: 2')
    status = db.Column(db.Integer, nullable=False, default=0, doc='状态。online:1, offline: 2')
    remark = db.Column(db.String(200), nullable=False, default='', doc='备注，如机器用做backup或etl等')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, gid, hid, ip, port, mem, persis, role, status, version='', remark=''):
        self.gid = gid
        self.hid = hid
        self.ip = ip
        self.port = port
        self.memory = mem
        self.persistence = persis
        self.version = version
        self.role = role
        self.status = status
        self.remark = remark

    def __repr__(self):
        return "<RedisInstance(id={}, gid={}, hid={}, port={})>".format(self.id, self.gid, self.hid, self.port)

db.Index('idx_gid_hid', RedisInstance.gid, RedisInstance.hid)
db.Index('idx_ip', RedisInstance.ip)


