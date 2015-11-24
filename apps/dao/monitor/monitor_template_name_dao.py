from sqlalchemy import or_

from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.monitor.monitor_template_name import MonitorTemplateName


class MonitorTemplateNameDao(GenericDAO):

    @classmethod
    def add(cls, o):
        db.session.add(o)
        db.session.commit()

    @classmethod
    def get_all_template_name(cls):
        return MonitorTemplateName.query.all()

    @classmethod
    def is_exist(cls, o):
        return MonitorTemplateName.query.filter(MonitorTemplateName.name == o.name).\
            filter(MonitorTemplateName.monitor_type == o.monitor_type).first()

    @classmethod
    def get_monitor_template_type_and_name(cls):
        return MonitorTemplateName.query.group_by(MonitorTemplateName.monitor_type, MonitorTemplateName.name).all()

    @classmethod
    def get_all_template_name_by_type(cls, o):
        return MonitorTemplateName.query.filter(MonitorTemplateName.monitor_type == o.monitor_type).all()
