from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.asset.group_type import GroupType


class GroupTypeDAO(GenericDAO):

    @classmethod
    def find(cls):
        pass

    @classmethod
    def add(cls, gt):
        db.session.add(gt)
        db.session.commit()

    @classmethod
    def update(cls):
        pass

    @classmethod
    def delete(cls):
        pass

    @classmethod
    def get_all_gtype_type(cls):
        return GroupType.query.with_entities(GroupType.type).all()

    @classmethod
    def get_all_gtypes(cls):
        return GroupType.query.all()

    @classmethod
    def get_gtype_by_type_name(cls, name):
        return GroupType.query.filter(GroupType.type == name).first()
