from sqlalchemy.orm import aliased

from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.config.monitor_template import MonitorTemplate


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
        return MonitorTemplate.query.with_entities(MonitorTemplate.name).distinct().all()

    @classmethod
    def get_monitor_template_info_by_name(cls, name):
        mt = aliased(MonitorTemplate)
        return MonitorTemplate.query.filter(mt.name == name).filter(mt.chart_name != '').\
            with_entities(mt.id, mt.ds_name, mt.ds_description, mt.chart_name, mt.chart_description).\
            order_by(mt.ds_name).all()

    @classmethod
    def get_monitor_template_type_and_name(cls):
        return MonitorTemplate.query.with_entities(MonitorTemplate.type, MonitorTemplate.name).\
            group_by(MonitorTemplate.type, MonitorTemplate.name).all()
