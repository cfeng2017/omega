from generic_dao import GenericDAO
from apps.dao.asset.group_type_dao import GroupTypeDAO
from apps.dao.asset.group_db_dao import GroupDbDAO
from apps.dao.asset.group_dao import GroupDAO
from apps.dao.asset.host_dao import HostDAO
from apps.dao.asset.mysql_instance_dao import MysqlInstanceDAO
from apps.dao.asset.mc_instance_dao import McInstanceDAO
from apps.dao.asset.redis_instance_dao import RedisInstanceDAO
from apps.dao.config.monitor_template_dao import MonitorTemplateDAO


class GenericDAOFactory(object):

    def __init__(self):
        super(GenericDAOFactory, self).__init__()

    @classmethod
    def new(cls):
        return GenericDAO()


class GroupTypeDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return GroupTypeDAO()


class GroupDbDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return GroupDbDAO()


class GroupDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return GroupDAO()


class HostDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return HostDAO()


class MysqlInstanceDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return MysqlInstanceDAO()


class McInstanceDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return McInstanceDAO()


class RedisInstanceDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return RedisInstanceDAO()


class MonitorTemplateDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return MonitorTemplateDAO()

