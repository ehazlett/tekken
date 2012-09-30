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
from flask import Flask
import logging

APP_NAME = 'tekken'
APP_VERSION = '0.1'
CACHE_TYPE = 'simple'
LOG_LEVEL = logging.DEBUG
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'tekken'
MONGO_USERNAME = None
MONGO_PASSWORD = None
MONGO_REPLICA_SET = None

# mongodb settings

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_PASSWORD = None
REDIS_EVENT_CHANNEL = 'nucleo'
REGISTRATION_CODES = []
REGISTRATION_ENABLED = True
SENSU_API_URL = 'http://localhost:4567'
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
