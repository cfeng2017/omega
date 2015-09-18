#! -*- coding: utf-8 -*-
from apps.service.generic_service import GenericService
from apps.dao.dao_factory import GroupDaoFactory, GroupTypeDaoFactory, GroupDbDaoFactory, \
    HostDaoFactory, MysqlInstanceDaoFactory, RedisInstanceDaoFactory, McInstanceDaoFactory
from apps.model.asset.group_type import GroupType
from apps.model.asset.group_db import GroupDb
from apps.model.asset.group import Group
from apps.model.asset.host import Host
from apps.model.asset.mysql_instance import MysqlInstance
from apps.model.asset.mc_instance import McInstance
from apps.model.asset.redis_instance import RedisInstance
from apps.model.common.logger import Logger


class AssetService(GenericService):

    def __init__(self):
        super(AssetService, self).__init__()

    @classmethod
    def new_dao(cls, o):
        if isinstance(o, GroupType):
            df = GroupTypeDaoFactory()
        elif isinstance(o, GroupDb):
            df = GroupDbDaoFactory()
        elif isinstance(o, Group):
            df = GroupDaoFactory()
        elif isinstance(o, Host):
            df = HostDaoFactory()
        elif isinstance(o, MysqlInstance):
            df = MysqlInstanceDaoFactory()
        elif isinstance(o, McInstance):
            df = McInstanceDaoFactory()
        elif isinstance(o, RedisInstance):
            df = RedisInstanceDaoFactory()
        else:
            Logger.error("Function new_dao() is failed, the object o is not belong to any class.")
            exit()
        return df.new()

    @classmethod
    def add(cls, o):
        AssetService.new_dao(o).add(o)

    @classmethod
    def get_all_gtype_type(cls):
        """
        :return: The group_types table's type, such as [(u'mysql'), (u'redis')].
        """
        dao = GroupTypeDaoFactory.new()
        return dao.get_all_gtype_type()

    @classmethod
    def get_all_gtypes(cls):
        """
        :return: all info of the group_types table, such as [GroupType(1, u'mysql'), GroupType(2, u'redis')]
        """
        dao = GroupTypeDaoFactory.new()
        return dao.get_all_gtypes()

    @classmethod
    def get_gtype_by_type_name(cls, name):
        dao = GroupTypeDaoFactory().new()
        return dao.get_gtype_by_type_name(name)

    @classmethod
    def get_all_groups(cls):
        dao = GroupDaoFactory.new()
        return dao.get_all_groups()

    @classmethod
    def get_group_by_type(cls, t=1):
        """
        :param t: Integer, which means group type, such as type of MYSQL is 1.
        :return: All groups which type is t in the groups table will be return, such as
                 [<Group(id=1, name=G1, type=1)>, <Group(id=2, name=G2, type=1)>] and so on.
        """
        dao = GroupDaoFactory.new()
        return dao.get_group_by_type(t)

    @classmethod
    def get_db_by_gid_and_name(cls, gid, db_name):
        dao = GroupDbDaoFactory().new()
        return dao.get_db_by_gid_and_name(gid, db_name)

    @classmethod
    def get_all_gdbs(cls):
        dao = GroupDbDaoFactory().new()
        return dao.get_all_gdbs()

    @classmethod
    def get_group_by_type_and_name(cls, gtype, name):
        dao = GroupDaoFactory().new()
        return dao.get_group_by_type_and_name(gtype, name)

    @classmethod
    def find_host_by_name_and_ip(cls, name, ip):
        dao = HostDaoFactory().new()
        return dao.find_host_by_name_and_ip(name, ip)

    @classmethod
    def get_hid_by_name(cls, name):
        dao = HostDaoFactory().new()
        return dao.get_hid_by_name(name)

    @classmethod
    def find_all_host_name_and_ip(cls):
        dao = HostDaoFactory().new()
        return dao.find_all_host_name_and_ip()

    @classmethod
    def find_mysql_instance_by_name_and_ip_and_port(cls, gid, hid, ip, port):
        dao = MysqlInstanceDaoFactory.new()
        return dao.find_mysql_instance_by_name_and_ip_and_port(gid, hid, ip, port)

    @classmethod
    def find_mc_instance_by_name_and_ip_and_port(cls, gid, hid, ip, port):
        dao = McInstanceDaoFactory.new()
        return dao.find_mc_instance_by_name_and_ip_and_port(gid, hid, ip, port)

    @classmethod
    def find_redis_instance_by_name_and_ip_and_port(cls, gid, hid, ip, port):
        dao = RedisInstanceDaoFactory().new()
        return dao.find_redis_instance_by_name_and_ip_and_port(gid, hid, ip, port)

    @classmethod
    def get_all_mysql_instance_info(cls):
        dao = MysqlInstanceDaoFactory().new()
        return dao.get_all_mysql_instance_info()

    @classmethod
    def get_all_mc_instance_info(cls):
        dao = McInstanceDaoFactory().new()
        return dao.get_all_mc_instance_info()

    @classmethod
    def get_all_redis_instance_info(cls):
        dao = RedisInstanceDaoFactory().new()
        return dao.get_all_redis_instance_info()