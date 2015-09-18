from generic_dao import GenericDAO
from apps.dao.asset.group_type_dao import GroupTypeDao
from apps.dao.asset.group_db_dao import GroupDbDao
from apps.dao.asset.group_dao import GroupDao
from apps.dao.asset.host_dao import HostDao
from apps.dao.asset.mysql_instance_dao import MysqlInstanceDao
from apps.dao.asset.mc_instance_dao import McInstanceDao
from apps.dao.asset.redis_instance_dao import RedisInstanceDao


class GenericDaoFactory(object):

    def __init__(self):
        super(GenericDaoFactory, self).__init__()

    @classmethod
    def new(cls):
        return GenericDAO()


class GroupTypeDaoFactory(GenericDaoFactory):

    @classmethod
    def new(cls):
        return GroupTypeDao()


class GroupDbDaoFactory(GenericDaoFactory):

    @classmethod
    def new(cls):
        return GroupDbDao()


class GroupDaoFactory(GenericDaoFactory):

    @classmethod
    def new(cls):
        return GroupDao()


class HostDaoFactory(GenericDaoFactory):

    @classmethod
    def new(cls):
        return HostDao()


class MysqlInstanceDaoFactory(GenericDaoFactory):

    @classmethod
    def new(cls):
        return MysqlInstanceDao()


class McInstanceDaoFactory(GenericDaoFactory):

    @classmethod
    def new(cls):
        return McInstanceDao()


class RedisInstanceDaoFactory(GenericDaoFactory):

    @classmethod
    def new(cls):
        return RedisInstanceDao()