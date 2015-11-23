from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.asset.group import Group


class GroupDAO(GenericDAO):

    @classmethod
    def find(cls):
        pass

    @classmethod
    def add(cls, group):
        db.session.add(group)
        db.session.commit()

    @classmethod
    def update(cls):
        pass

    @classmethod
    def delete(cls):
        pass

    @classmethod
    def get_all_groups(cls):
        return Group.query.order_by(Group.type, Group.id).all()

    @classmethod
    def get_group_by_type(cls, t):
        return Group.query.filter(Group.type == t).all()

    @classmethod
    def get_group_by_type_and_name(cls, gtype, name):
        return Group.query.filter(Group.type == gtype, Group.name == name).all()

