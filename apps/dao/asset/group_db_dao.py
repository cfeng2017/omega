from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.asset.group_db import GroupDb
from apps.model.asset.group import Group


class GroupDbDao(GenericDAO):

    @classmethod
    def find(cls):
        pass

    @classmethod
    def add(cls, gdb):
        db.session.add(gdb)
        db.session.commit()

    @classmethod
    def update(cls):
        pass

    @classmethod
    def delete(cls):
        pass

    @classmethod
    def get_db_by_gid_and_name(cls, gid, db_name):
        return GroupDb.query.filter(GroupDb.gid == gid, GroupDb.db == db_name).all()

    @classmethod
    def get_all_gdbs(cls):
        return GroupDb.query.with_entities(GroupDb.gid, Group.name, GroupDb.db).\
            filter(Group.id == GroupDb.gid).all()


