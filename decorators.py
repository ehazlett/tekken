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
from functools import wraps
from flask import request, current_app, redirect, url_for
from flask import session
import messages
from utils import generate_api_response
from utils import db

def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('api-key')
        # validate
        if not api_key:
            data = {'error': messages.NO_API_KEY}
            return generate_api_response(data, 401)
        user = db.get_user({'api_key': api_key})
        if not user:
            data = {'error': messages.INVALID_API_KEY}
            return generate_api_response(data, 401)
        session['user'] = user
        return f(*args, **kwargs)
    return decorated

def internal_api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('api-key')
        # validate
        if not api_key:
            data = {'error': messages.NO_API_KEY}
            return generate_api_response(data, 401)
        if api_key not in current_app.config.get('INTERNAL_API_KEYS'):
            data = {'error': messages.INVALID_API_KEY}
            return generate_api_response(data, 401)
        session['internal_api_key'] = api_key
        return f(*args, **kwargs)
    return decorated

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('accounts.login') + '?next={0}'.format(request.path))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = session.get('user', {})
        if not user or not user.get('is_admin'):
            return redirect(url_for('accounts.login') + '?next={0}'.format(request.path))
        return f(*args, **kwargs)
    return decorated
