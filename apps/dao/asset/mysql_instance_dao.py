# -*- coding: utf8 -*-
from sqlalchemy import or_, distinct
from sqlalchemy.orm import aliased

from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.asset.mysql_instance import MysqlInstance
from apps.model.asset.group import Group
from apps.model.asset.host import Host
from apps.model.monitor.monitor_template_name import MonitorTemplateName


class MysqlInstanceDAO(GenericDAO):

    @classmethod
    def find(cls):
        pass

    @classmethod
    def add(cls, instance):
        db.session.add(instance)
        db.session.commit()

    @classmethod
    def update(cls):
        pass

    @classmethod
    def delete(cls):
        pass

    @classmethod
    def find_mysql_instance_by_name_and_port(cls, gid, hid, port):
        return MysqlInstance.query.filter(MysqlInstance.gid == gid,
                                          MysqlInstance.hid == hid,
                                          MysqlInstance.port == port).all()

    @classmethod
    def get_all_mysql_instance_info(cls):
        mi = aliased(MysqlInstance)
        return MysqlInstance.query.filter(mi.gid == Group.id, mi.hid == Host.id).\
            with_entities(mi.id, mi.gid, Group.name, mi.hid, Host.host, mi.port,
                          mi.version, mi.role, mi.status, mi.remark).order_by(mi.gid).all()

    @classmethod
    def get_all_online_infos(cls, gtypes):
        i, h = MysqlInstance, Host
        return MysqlInstance.query.with_entities(i.gid, i.hid, i.id, h.host, h.ip, i.port, i.role).\
            filter(i.hid == h.id, i.status == 1, i.gid.in_(gtypes)).order_by(i.gid).all()

    """
    返回Mysql机器的id，hostname，status
    """
    @classmethod
    def get_all_hosts(cls):
        mi = aliased(MysqlInstance)
        return MysqlInstance.query.with_entities(distinct(mi.hid), Host.host, Host.status).\
            filter(mi.hid == Host.id).order_by(mi.id).all()
