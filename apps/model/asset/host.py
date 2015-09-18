#! -*- encoding: utf-8 -*-
from apps import db


class Host(db.Model):
    __tablename__ = 't_host'

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(32), nullable=False, default='')
    core = db.Column(db.Integer, nullable=False, default='0', doc='cpu核数')
    memory = db.Column(db.Integer, nullable=False, default='0', doc='内存大小，以G为单位')
    disk = db.Column(db.String(200), nullable=False, default='0',
                     doc='磁盘信息，JSON字符串，内容为(磁盘类型，个数，每类磁盘大小)形式，磁盘类型：SAS: 0,SSD: 1,SATA: 2')
    eth = db.Column(db.String(10), nullable=False, default='', doc='主要网卡设备名')
    ip = db.Column(db.String(15), nullable=False, default='', doc='主要网卡IP')
    oips = db.Column(db.String(192), nullable=False, default='', doc='其他网卡信息，json字符串，内容为(设备名，ip)形式')
    remote_ip = db.Column(db.String(32), nullable=False, default='', doc='远程控制卡ip')
    idc = db.Column(db.SmallInteger, nullable=False, default='0', doc='idc机房，天津机房：0，IDC10：1, 为IDC20：2')
    rack = db.Column(db.String(10), nullable=False, default='', doc='机架位置')
    bbu_relearn_flag = db.Column(db.SmallInteger, nullable=False,
                                 default='0', doc='电池充放电。不手动充放:0，手动充放:1')
    bbu_relearn_date = db.Column(db.DateTime, nullable=False, default='1000-01-01 00:00:00')
    status = db.Column(db.SmallInteger, nullable=False, default='0', doc='机器状态。offline:0，online:1')
    remark = db.Column(db.String(200), nullable=False, default='', doc='机器备注')
    updatetime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.FetchedValue(),
                           server_onupdate=db.FetchedValue())

    def __init__(self, host='', core=0, memory=0, disk='', eth='', ip='', oips='', rip='', idc=0, rack=0,
                 brf=0, brd='', status=0, remark=''):
        self.host = host
        self.cores = core
        self.memory = memory
        self.disk = disk
        self.eth = eth
        self.ip = ip
        self.oips = oips
        self.remote_ip = rip
        self.idc = idc
        self.rack = rack
        self.bbu_relearn_flag = brf
        self.bbu_relearn_date = brd
        self.status = status
        self.remark = remark

    def __repr__(self):
        return "<Group(id={}, host={}, ip={})>".format(self.id, self.host, self.ip)

db.Index('idx_host', Host.host, unique=True)
db.Index('idx_ip', Host.ip, unique=True)

