# -*- conding: utf-8 -*-

from asset_service import GenericService
from apps.dao.dao_factory import MonitorTemplateDAOFactory
from apps.model.config.monitor_template import MonitorTemplate
from apps.model.common.logger import Logger


class ConfigService(GenericService):

    def __init__(self):
        super(ConfigService, self).__init__()

    @classmethod
    def new_dao(cls, o):
        if isinstance(o, MonitorTemplate):
            mtf = MonitorTemplateDAOFactory()
        else:
            Logger.error("Function new_dao() is failed, the object o is not belong to any class.")
            return None
        return mtf.new()

    @classmethod
    def add(cls, o):
        if o:
            ConfigService.new_dao(o).add(o)
        else:
            Logger.error("{} is None, please check it!")

    @classmethod
    def addmany(cls, o):
        if o:
            ConfigService.new_dao(o[0]).addmany(o)
        else:
            ConfigService.add(o)

    @classmethod
    def find(cls, o):
        dao = ConfigService.new_dao(o)

    @classmethod
    def is_exist(cls, o):
        dao = ConfigService.new_dao(o)
        return dao.is_exist(o)

    @classmethod
    def get_all_template_name(cls, name):
        """
        :return: [(u'monitor_template1',), (u'monitor_template2',)]
        """
        dao = ConfigService.new_dao(name)
        return dao.get_all_template_name()

    @classmethod
    def get_monitor_template_info_by_name(cls, name):
        dao = MonitorTemplateDAOFactory().new()
        return dao.get_monitor_template_info_by_name(name)

    @classmethod
    def get_monitor_template_type_and_name(cls):
        dao = MonitorTemplateDAOFactory().new()
        return dao.get_monitor_template_type_and_name()