from apps import db
from apps.dao.generic_dao import GenericDAO


class InstanceDao(GenericDAO):

    @classmethod
    def find(cls):
        pass

    @classmethod
    def add(cls, instance):
        db.session.add(instance)

    @classmethod
    def update(cls):
        pass

    @classmethod
    def delete(cls):
        pass
