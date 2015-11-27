from generic_dao import GenericDAO
from apps.dao.asset.group_type_dao import GroupTypeDAO
from apps.dao.asset.group_db_dao import GroupDbDAO
from apps.dao.asset.group_dao import GroupDAO
from apps.dao.asset.host_dao import HostDAO
from apps.dao.asset.mysql_instance_dao import MysqlInstanceDAO
from apps.dao.asset.mc_instance_dao import McInstanceDAO
from apps.dao.asset.redis_instance_dao import RedisInstanceDAO
from apps.dao.monitor.monitor_template_dao import MonitorTemplateDAO
from apps.dao.monitor.monitor_template_name_dao import MonitorTemplateNameDao
from apps.dao.monitor.chart_dao import ChartDao
from apps.dao.monitor.ds_dao import DsDao
from apps.dao.monitor.monitor_alarm_dao import MonitorAlarmDao


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


class MonitorTemplateNameDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return MonitorTemplateNameDao()


class ChartDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return ChartDao()


class DsDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return DsDao()


class MonitorAlarmDAOFactory(GenericDAOFactory):

    @classmethod
    def new(cls):
        return MonitorAlarmDao()
