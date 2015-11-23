from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.asset.host import Host
from sqlalchemy import or_


class HostDAO(GenericDAO):

    @classmethod
    def find(cls):
        pass

    @classmethod
    def add(cls, host):
        db.session.add(host)
        db.session.commit()

    @classmethod
    def update(cls):
        pass

    @classmethod
    def delete(cls):
        pass

    @classmethod
    def find_host_by_name_and_ip(cls, name, ip):
        return Host.query.filter(or_(Host.host == name, Host.ip == ip)).first()

    @classmethod
    def find_all_host_name_and_ip(cls):
        return Host.query.with_entities(Host.id, Host.host, Host.ip, Host.remote_ip).order_by(Host.id).all()

    @classmethod
    def get_hid_by_name(cls, name):
        return Host.query.with_entities(Host.id).filter(Host.host == name).first()
