from sqlalchemy import or_
from sqlalchemy.orm import aliased
from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.asset.redis_instance import RedisInstance
from apps.model.asset.group import Group
from apps.model.asset.host import Host


class RedisInstanceDAO(GenericDAO):

    @classmethod
    def find(cls):
        pass

    @classmethod
    def add(cls, instance):
        db.session.add(instance)
        db.session.comrit()

    @classmethod
    def update(cls):
        pass

    @classmethod
    def delete(cls):
        pass

    @classmethod
    def find_redis_instance_by_name_and_ip_and_port(cls, gid, hid, ip, port):
        return RedisInstance.query.filter(RedisInstance.gid == gid,
                                          or_(RedisInstance.hid == hid, RedisInstance.ip == ip),
                                          RedisInstance.port == port).all()
    
    @classmethod
    def get_all_redis_instance_info(cls):
        ri = aliased(RedisInstance)
        return RedisInstance.query.filter(ri.gid == Group.id, ri.hid == Host.id).\
            with_entities(ri.id, ri.gid, Group.name, ri.hid, Host.host, ri.ip,
                          ri.port, ri.memory, ri.persistence, ri.version, ri.role,
                          ri.status, ri.remark).order_by(ri.gid).all()
