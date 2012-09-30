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
import hashlib
from flask import current_app, request, Response, json
from bson import json_util
import yaml
from urlparse import urlparse, urljoin
from flask.ext.mail import Message
import config

def get_redis_connection():
    """
    Returns a Redis connection for the current app

    """
    return current_app.config.get('redis')

def get_mongo_connection():
    """
    Returns a MongoDB connection for the current app
    """
    try:
        mdb = current_app.config.get('mongo')
    except RuntimeError:
        # probably not running in context ; attempt to build connection manually
        # this is some major hackery -- just run from the fucking context if you can ;)
        from pymongo import Connection
        import config
        conn = Connection(host=getattr(config, 'MONGO_HOST'), port=getattr(config, 'MONGO_PORT'))
        db = conn[getattr(config, 'MONGO_DBNAME')]
        username = getattr(config, 'MONGO_USERNAME')
        if username:
            db.authenticate(username, getattr(config, 'MONGO_PASSWORD'))
        # HACK: create an object to fulfill what other functions are expecting
        class Mdb(object):
            pass
        mdb = Mdb()
        setattr(mdb, 'db', db)
    return mdb

def generate_api_response(data, status=200, content_type='application/json'):
    """
    `flask.Response` factory for api responses

    :param data: Data that gets serialized to JSON
    :param status: Status code (default: 200)
    :param content_type: Content type (default: application/json)

    """
    indent = None
    if request.args.get('indent'):
        indent = 2
    # check if need to add status_code
    if data == type({}) and not data.has_key('status_code'):
        data['status_code'] = status
    # serialize
    if type(data) != type(''):
        data = json.dumps(data, sort_keys=True, indent=indent, default=json_util.default)
    resp = Response(data, status=status, content_type=content_type)
    return resp

def generate_yaml_response(data, status=200, content_type='application/yaml'):
    data = yaml.safe_dump(data, explicit_start=True, default_flow_style=False)
    resp = Response(data, status=status, content_type=content_type)
    return resp

def hash_text(text):
    """
    Hashes text with app key

    :param text: Text to encrypt

    """
    h = hashlib.sha256()
    h.update(getattr(config, 'SECRET_KEY'))
    h.update(text)
    return h.hexdigest()

def send_mail(subject=None, text=None, to=[]):
    """
    Sends mail

    :param subject: Subject
    :param text: Message
    :param to: Recipients as list

    """
    mail = current_app.config.get('mail')
    msg = Message(subject, sender=current_app.config.get('DEFAULT_SENDER'), \
        recipients=to)
    msg.body = text
    return mail.send(msg)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    next_url = request.values.get('next')
    if next_url and is_safe_url(next_url):
        return next_url

class MongoPaginator(object):
    def __init__(self, objs):
        self._objs = objs
        limit = abs(int(request.args.get('limit', 15)))
        page = abs(int(request.args.get('page', 0)))
        skip = (limit * page) # calc where to start
        total = objs.count()
        objs.skip(skip).limit(limit)
        has_next = total > (objs.count(with_limit_and_skip=True) * (page+1))
        self.has_prev = page
        self.has_next = has_next
        self.prev_page = page - 1
        self.next_page = page + 1

