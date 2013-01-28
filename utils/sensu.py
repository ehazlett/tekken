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
from flask import json, current_app
import requests

URL_BASE = '{0}'

def _request(path='', method='get', data=None, username=None):
    """
    Wrapper function for Sensu API requests

    :param path: URL to request
    :param method: HTTP method
    :param data: Data for post (ignored for GETs)
    :param username: (optional) User for which to proxy

    """
    method = method.lower()
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
    }
    methods = {
        'get': requests.get,
        'post': requests.post,
        'delete': requests.delete,
    }
    url = '{0}{1}'.format(URL_BASE.format(current_app.config.get('SENSU_API_URL')), path)
    return methods[method](url, data=json.dumps(data), headers=headers)

def get_info():
    """
    Gets Sensu server info

    """
    r = _request('/info')
    try:
        data = json.loads(r.content)
    except:
        data = {}
    return data

def get_events():
    """
    Gets the current Sensu events

    """
    r = _request('/events')
    try:
        data = json.loads(r.content)
    except:
        data = {}
    return data

def resolve_event(client=None, check=None):
    """
    Resolves a Sensu event

    :param client: Client name
    :param check: Sensu check

    """
    payload = {
        'client': client,
        'check': check,
    }
    r = _request('/event/resolve', method='post', data=payload)
    try:
        data = json.loads(r.content)
    except:
        data = {}
    return data

def get_clients():
    """
    Gets the Sensu clients

    """
    r = _request('/clients')
    try:
        data = json.loads(r.content)
    except:
        data = {}
    return data

def delete_client(name=None):
    """
    Deletes a Sensu client
    
    :param name: Client name

    """
    r = _request('/clients/{0}'.format(name), method='delete')
    try:
        data = json.loads(r.content)
    except:
        data = {}
    return data

def get_checks():
    """
    Gets the Sensu checks

    """
    r = _request('/checks')
    try:
        data = json.loads(r.content)
    except:
        data = {}
    return data

def get_stashes():
    """
    Gets the Sensu stashes

    """
    r = _request('/stashes')
    try:
        data = json.loads(r.content)
    except:
        data = {}
    return data

def get_stash(key):
    """
    Gets the specified Sensu stash

    """
    r = _request('/stashes/{0}'.format(key))
    try:
        data = json.loads(r.content)
    except:
        data = {}
    return data

def create_stash(key=None, description=''):
    """
    Creates a Sensu stash

    :param key: Stash key
    :param description: Stash description

    """
    payload = {
        'key': key,
        'description': description,
    }
    r = _request('/stashes/{0}'.format(key), method='post', data=payload)
    try:
        data = json.loads(r.content)
    except:
        data = {}
    return data

def delete_stash(key=None):
    """
    Deletes a Sensu stash
    
    :param key: Stash key to delete

    """
    r = _request('/stashes/{0}'.format(key), method='delete')
    try:
        data = json.loads(r.content)
    except:
        data = {}
    return data

