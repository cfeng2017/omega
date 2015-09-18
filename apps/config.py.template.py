#! -*- coding: utf-8 -*-

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql://dev_username:dev_password@dev_ip/dev_database"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://pd_username:pd_password@pd_ip/pd_database"

class DevConfig(Config):
    DEBUG = True
