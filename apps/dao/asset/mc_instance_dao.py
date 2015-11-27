from sqlalchemy import or_
from sqlalchemy.orm import aliased
from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.asset.mc_instance import McInstance
from apps.model.asset.host import Host
from apps.model.asset.group import Group


class McInstanceDAO(GenericDAO):

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
    def find_mc_instance_by_name_and_port(cls,  gid, hid, port):
        return McInstance.query.filter(McInstance.gid == gid,
                                       McInstance.hid == hid,
                                       McInstance.port == port).all()

    @classmethod
    def get_all_mc_instance_info(cls):
        mi = aliased(McInstance)
        return McInstance.query.filter(mi.gid == Group.id, mi.hid == Host.id).\
            with_entities(mi.id, mi.gid, Group.name, mi.hid, Host.host, mi.port,
                          mi.memory, mi.thread, mi.maxconn, mi.factor, mi.parameters, mi.user,
                          mi.version, mi.role, mi.status, mi.remark).order_by(mi.gid).all()
