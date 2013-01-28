#!/usr/bin/env python
# Copyright 2012 Tekken Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from flask import Flask, json
import logging

APP_NAME = 'tekken'
APP_VERSION = '0.1'
CACHE_TYPE = 'simple'
LOG_LEVEL = logging.DEBUG
if os.environ.has_key('VCAP_SERVICES'):
    cfg = json.loads(os.environ.get('VCAP_SERVICES'))
    mdb = cfg.get('mongodb-2.0', {})
    mdb_creds = mdb[0].get('credentials', {})
    MONGO_HOST = mdb_creds.get('hostname')
    MONGO_PORT = mdb_creds.get('port')
    MONGO_DBNAME = mdb_creds.get('db')
    MONGO_USERNAME = mdb_creds.get('username')
    MONGO_PASSWORD = mdb_creds.get('password')
    rds = cfg.get('redis-2.6', {})
    rds_creds = rds[0].get('credentials', {})
    REDIS_HOST = rds_creds.get('hostname')
    REDIS_PORT = rds_creds.get('port')
    REDIS_DB = 0
    REDIS_PASSWORD = rds_creds.get('password')
else:
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'tekken'
    MONGO_USERNAME = None
    MONGO_PASSWORD = None
    MONGO_REPLICA_SET = None
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 1
    REDIS_PASSWORD = None
REGISTRATION_CODES = []
REGISTRATION_ENABLED = True
SENSU_API_URL = 'http://127.0.0.1:4567'
SENTRY_DSN = None
SECRET_KEY = '1q2w3e4r5t6y7u8i9o0p'

def create_app():
    """
    Flask app factory

    :rtype: `flask.Flask`

    """
    app = Flask(__name__)
    app.config.from_object('config')
    #sentry.init_app(app)
    return app

try:
    from local_config import *
except ImportError:
    pass
