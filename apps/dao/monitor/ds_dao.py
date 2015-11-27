# -*- coding: utf8 -*-
from sqlalchemy.orm import aliased

from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.monitor.ds import Ds


class DsDao(GenericDAO):

    @classmethod
    def add(cls, o):
        db.session.add(o)
        db.session.commit()

    @classmethod
    def addmany(cls, o):
        db.session.bulk_save_objects(o)
        db.session.commit()

    @classmethod
    def get_ds_by_chart_id_list(cls, cid_list):
        return Ds.query.filter(Ds.chart_id.in_(cid_list)).all()
