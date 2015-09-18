#!/usr/bin/python
import sys

from os.path import dirname, abspath

# pro_path = dirname(dirname(dirname(abspath(__file__))))
asset_path = dirname(abspath(__file__)) + '/asset'
sys.path.append(asset_path)

from apps.model.asset.mysql_instance import MysqlInstance
from apps import db
db.create_all()


