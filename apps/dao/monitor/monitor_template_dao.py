# -*- coding: utf8 -*-
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
    # def is_exist(cls, o):
    #     return MonitorTemplate.query.filter(MonitorTemplate.name == o.name).first()

    @classmethod
    def get_all_template_name(cls):
        return MonitorTemplate.query.with_entities(MonitorTemplate.template_name_id == MonitorTemplateName.id).\
            distinct().all()

    @classmethod
    def get_monitor_template_info(cls, o):
        m = aliased(MonitorTemplate)
        return MonitorTemplate.query.filter(m.template_name_id == o.template_name_id).\
            with_entities(m.id, m.chart_name, m.chart_description, m.ds_name, m.ds_description).\
            order_by(m.chart_name).all()

    """
    通过template_id获取monitor_template表的所有信息。
    返回值: [(<MonitorTemplate(id, template_name_id, ds_name, ds_description, chart_name, chart_description, status, ...)>)]
    """
    @classmethod
    def get_charts_by_template_id(cls, tid):
        return MonitorTemplate.query.filter(MonitorTemplate.template_name_id == tid).all()
