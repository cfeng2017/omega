#! -*- encoding: utf8 -*-
from apps import db


class McInstance(db.Model):
    __tablename__ = 't_mc_instance'

    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.Integer, nullable=False, doc='组id')
    hid = db.Column(db.Integer, nullable=False, doc='主机id')
    ip = db.Column(db.String(256), nullable=False, doc='ip')
    port = db.Column(db.Integer, nullable=False, doc='端口号')
    memory = db.Column(db.Integer, nullable=False, doc='分配内存，单位MB')
    thread = db.Column(db.Integer, nullable=False, doc='分配进程数')
    maxconn = db.Column(db.Integer, nullable=False, doc='最大连接数')
    factor = db.Column(db.Integer, nullable=False, doc='增长因子')
    parameters = db.Column(db.String(100), nullable=False, default='', doc='其他参数，如-o slab_automove 等')
    role = db.Column(db.Integer, nullable=False, default=0, doc='角色，master:1, slave: 2')
    status = db.Column(db.Integer, nullable=False, default=0, doc='状态。online:1, offline: 2')
    user = db.Column(db.String(20), nullable=False, default='memcached', doc='运行的用户名')
    version = db.Column(db.String(20), nullable=False, doc='版本号')
    remark = db.Column(db.String(200), nullable=False, default='', doc='备注，如机器用做backup或etl等')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, gid, hid, ip, port, mem, thread, mconn, factor,
                 par, role, status, user='memcached', version='', remark=''):
        self.gid = gid
        self.hid = hid
        self.ip = ip
        self.port = port
        self.memory = mem
        self.thread = thread
        self.maxconn = mconn
        self.factor = factor
        self.version = version
        self.parameters = par
        self.role = role
        self.user = user
        self.status = status
        self.remark = remark

    def __repr__(self):
        return "<McInstance(id={}, gid={}, hid={}, port={})>".format(self.id, self.gid, self.hid, self.port)

db.Index('idx_gid_hid', McInstance.gid, McInstance.hid)
db.Index('idx_ip', McInstance.ip)

