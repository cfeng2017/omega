from sqlalchemy import or_
from sqlalchemy.orm import aliased

from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.asset.mysql_instance import MysqlInstance
from apps.model.asset.group import Group
from apps.model.asset.host import Host


class MysqlInstanceDao(GenericDAO):

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
    def find_mysql_instance_by_name_and_ip_and_port(cls, gid, hid, ip, port):
        return MysqlInstance.query.filter(MysqlInstance.gid == gid,
                                          or_(MysqlInstance.hid == hid, MysqlInstance.ip == ip),
                                          MysqlInstance.port == port).all()

    @classmethod
    def get_all_mysql_instance_info(cls):
        mi = aliased(MysqlInstance)
        return MysqlInstance.query.filter(mi.gid == Group.id, mi.hid == Host.id).\
            with_entities(mi.id, mi.gid, Group.name, mi.hid, Host.host, mi.ip, mi.port,
                          mi.version, mi.role, mi.status, mi.remark).order_by(mi.gid).all()

