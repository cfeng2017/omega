# -*- conding: utf-8 -*-

from asset_service import GenericService
from apps.dao.dao_factory import MonitorTemplateDAOFactory, MonitorTemplateNameDAOFactory
from apps.model.monitor.monitor_template import MonitorTemplate
from apps.model.monitor.monitor_template_name import MonitorTemplateName
from apps.model.common.logger import Logger


class ConfigService(GenericService):

    def __init__(self):
        super(ConfigService, self).__init__()

    @classmethod
    def new_dao(cls, o):
        if isinstance(o, MonitorTemplate):
            mtf = MonitorTemplateDAOFactory()
        elif isinstance(o, MonitorTemplateName):
            mtf = MonitorTemplateNameDAOFactory()
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
    def get_all_template_name_by_type(cls, mt):
        """
        :return: [(u'monitor_template1',), (u'monitor_template2',)]
        """
        dao = ConfigService.new_dao(mt)
        return dao.get_all_template_name_by_type(mt)

    @classmethod
    def get_monitor_template_info(cls, mt):
        dao = ConfigService.new_dao(mt)
        return dao.get_monitor_template_info(mt)

    @classmethod
    def get_monitor_template_type_and_name(cls):
        dao = MonitorTemplateNameDAOFactory().new()
        result = dao.get_monitor_template_type_and_name()
        m_flag, type_list, _ = result[0].monitor_type if result else '', [], []
        for r in result:
            if str(m_flag) != str(r.monitor_type):
                tn = ({'type': m_flag, 'names': _})
                type_list.append(tn)
                m_flag = r.monitor_type
                _ = []
            _.append((r.id, r.name))
        tn = ({'type': m_flag, 'names': _})
        type_list.append(tn)
        return type_list

    @classmethod
    def get_all_monitor_template_type(cls):
        dao = MonitorTemplateNameDAOFactory().new()
        return dao.get_all_monitor_template_type()