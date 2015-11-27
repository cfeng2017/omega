# -*- coding: utf8 -*-
from sqlalchemy.orm import aliased

from apps import db
from apps.dao.generic_dao import GenericDAO
from apps.model.monitor.monitor_alarm import MonitorAlarm


class MonitorAlarmDao(GenericDAO):

    @classmethod
    def add(cls, o):
        db.session.add(o)
        db.session.commit()

    @classmethod
    def addmany(cls, o):
        db.session.bulk_save_objects(o)
        db.session.commit()


