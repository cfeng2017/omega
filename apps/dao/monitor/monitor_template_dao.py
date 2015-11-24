from sqlalchemy.orm import aliased

from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.monitor.monitor_template import MonitorTemplate
from apps.model.monitor.monitor_template_name import MonitorTemplateName


class MonitorTemplateDAO(GenericDAO):

    @classmethod
    def add(cls, o):
        db.session.add(o)
        db.session.commit()

    @classmethod
    def addmany(cls, o):
        db.session.bulk_save_objects(o)
        db.session.commit()

    @classmethod
    def find(cls):
        pass

    @classmethod
    def is_exist(cls, o):
        return MonitorTemplate.query.filter(MonitorTemplate.name == o.name).first()

    @classmethod
    def get_all_template_name(cls):
        return MonitorTemplate.query.with_entities(MonitorTemplate.template_id == MonitorTemplateName.id).\
            distinct().all()

    @classmethod
    def get_monitor_template_info(cls, o):
        m = aliased(MonitorTemplate)
        return MonitorTemplate.query.filter(m.template_id == o.template_id).\
            with_entities(m.id, m.chart_name, m.chart_description, m.ds_name, m.ds_description).\
            order_by(m.chart_name).all()

    # @classmethod
    # def get_monitor_template_info_by_name(cls, name):
    #     mt = aliased(MonitorTemplate)
    #     return MonitorTemplate.query.filter(mt.name == name).filter(mt.chart_name != '').\
    #         with_entities(mt.id, mt.ds_name, mt.ds_description, mt.chart_name, mt.chart_description).\
    #         order_by(mt.ds_name).all()

    # @classmethod
    # def get_monitor_template_type_and_name(cls):
    #     return MonitorTemplate.query.with_entities(MonitorTemplateName.name).\
    #         filter(MonitorTemplate.template_id == MonitorTemplateName.id).\
    #         group_by(MonitorTemplate.template_id).all()
