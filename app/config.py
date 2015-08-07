#! -*- coding: utf-8 -*-

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ""

class ProductionConfig(Config):
    DATABASE_URI = ""

class DevConfig(Config):
    DEBUG = True
