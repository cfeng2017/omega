# -*- coding: utf8 -*-
from sqlalchemy.orm import aliased

from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.monitor.chart import Chart
from apps.model.monitor.monitor_template_name import MonitorTemplateName


class ChartDao(GenericDAO):

    @classmethod
    def add(cls, o):
        db.session.add(o)
        db.session.commit()

    @classmethod
    def addmany(cls, o):
        db.session.bulk_save_objects(o)
        db.session.commit()

    @classmethod
    def get_chart_name_and_description_by_template_id_and_hid_list(cls, tid, hid_list):
        return Chart.query.with_entities(Chart.id, Chart.hid, Chart.name, Chart.description).\
            filter(Chart.template_name_id == tid, Chart.hid.in_(hid_list)).all()

    @classmethod
    def get_tmeplate_by_hid_list(cls, hid_list):
        mt = aliased(MonitorTemplateName)
        return Chart.query.with_entities(Chart.id, Chart.hid, mt.id, mt.name).\
            filter(Chart.hid.in_(hid_list), Chart.template_name_id == mt.id).all()

    @classmethod
    def is_exist(cls, tid, hid):
        return Chart.query.filter(Chart.template_name_id == tid, Chart.hid == hid).first()

    @classmethod
    def get_charts_by_hid(cls, hid):
        return Chart.query.with_entities(Chart.id, Chart.name, Chart.description, Chart.hid)\
            .filter(Chart.hid == hid).all()
