# -*- coding: utf-8 -*-

from apps.service.generic_service import GenericService
from apps.model.asset.group import Group
from apps.model.asset.group_db import GroupDb
from apps.model.asset.group_type import GroupType
from apps.model.asset.host import Host
from apps.model.asset.mysql_instance import MysqlInstance
from apps.model.asset.redis_instance import RedisInstance
from apps.model.asset.mc_instance import McInstance
from apps.dao.dao_factory import GroupDAOFactory, GroupTypeDAOFactory, GroupDbDAOFactory, \
    HostDAOFactory, MysqlInstanceDAOFactory, RedisInstanceDAOFactory, McInstanceDAOFactory, \
    MonitorTemplateNameDAOFactory, MonitorTemplateDAOFactory, DsDAOFactory, ChartDAOFactory, \
    MonitorAlarmDAOFactory
from apps.model.monitor.monitor_template_name import MonitorTemplateName
from apps.model.monitor.monitor_template import MonitorTemplate
from apps.model.monitor.chart import Chart
from apps.model.monitor.ds import Ds
from apps.model.monitor.monitor_alarm import MonitorAlarm
from apps.model.common.logger import Logger


class MonitorService(GenericService):

    def __init__(self):
        super(MonitorService, self).__init__()

    @classmethod
    def new_dao(cls, o):
        if isinstance(o, GroupType):
            df = GroupTypeDAOFactory()
        elif isinstance(o, GroupDb):
            df = GroupDbDAOFactory()
        elif isinstance(o, Group):
            df = GroupDAOFactory()
        elif isinstance(o, Host):
            df = HostDAOFactory()
        elif isinstance(o, MysqlInstance):
            df = MysqlInstanceDAOFactory()
        elif isinstance(o, McInstance):
            df = McInstanceDAOFactory()
        elif isinstance(o, RedisInstance):
            df = RedisInstanceDAOFactory()
        elif isinstance(o, MonitorTemplateName):
            df = MonitorTemplateNameDAOFactory()
        elif isinstance(o, Chart):
            df = ChartDAOFactory()
        elif isinstance(o, Ds):
            df = DsDAOFactory()
        elif isinstance(o, MonitorAlarm):
            df = MonitorAlarmDAOFactory()
        else:
            Logger.error("Function new_dao() is failed, the object o is not belong to any class.")
            exit()
        return df.new()

    def get_groups_by_type(self, gtype):
        dao = GroupDAOFactory().new()
        return dao.get_groups_by_type(gtype)

    def get_all_online_infos(self, instance, types):
        dao = MonitorService().new_dao(instance)
        return dao.get_all_online_infos(types)

    def get_all_hosts(self, o):
        dao = MonitorService().new_dao(o)
        return dao.get_all_hosts()

    def get_all_monitor_template_type(self):
        dao = MonitorTemplateNameDAOFactory.new()
        return dao.get_all_monitor_template_type()

    def get_all_template_name_by_type(self, o):
        dao = MonitorService().new_dao(o)
        return dao.get_all_template_name_by_type(o)

    def get_charts_by_template_id(self, tid):
        dao = MonitorTemplateDAOFactory().new()
        return dao.get_charts_by_template_id(tid)

    @classmethod
    def add(cls, o):
        if o:
            MonitorService().new_dao(o).add(o)
        else:
            Logger.error("{} is None, please check it!")

    @classmethod
    def addmany(cls, o):
        if o:
            MonitorService().new_dao(o[0]).addmany(o)
        else:
            MonitorService().add(o)

    @classmethod
    def get_chart_name_and_description_by_template_id_and_hid_list(cls, tid, hid_list):
        """通过hid列表获取chart表的id, name, description
        返回类型：[(id, hid, name, description)]
        """
        dao = ChartDAOFactory().new()
        return dao.get_chart_name_and_description_by_template_id_and_hid_list(tid, hid_list)

    @classmethod
    def get_tmeplate_by_hid_list(cls, hid_list):
        """返回关联的模板信息
        返回值：[(id, hid, template_name_id, tempalte_name)]
        """
        dao = ChartDAOFactory().new()
        return dao.get_tmeplate_by_hid_list(hid_list)

    @classmethod
    def is_exist(cls, tid, hid):
        """通过模板名id和主机id判断主机与模板是否已关联

        参数：
            tid: monitor_template_name的id
            hid: host id
        返回值: <Chart(id, name, description)>
        """
        dao = ChartDAOFactory().new()
        return dao.is_exist(tid, hid)

    @classmethod
    def get_charts_by_hid(cls, hid):
        """通过hid获取chart表的信息

        参数：
            hid: host id
        返回值：
            内容为((id, name, description, hid))的tuple。其中id，name, description分别为chart的id，name和description
        """
        dao = ChartDAOFactory().new()
        return dao.get_charts_by_hid(hid)

    @classmethod
    def get_ds_by_chart_id_list(cls, cid_list):
        """获取chart_id_list中各chart_id的ds信息

        参数：
            cid_list: chart id list
        返回值：
            [(<Ds(id, name, description, chart_id)>)]
        """
        dao = DsDAOFactory().new()
        return dao.get_ds_by_chart_id_list(cid_list)

