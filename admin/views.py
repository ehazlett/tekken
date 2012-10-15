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
from flask import Blueprint
from flask import (request, render_template, jsonify, g, flash, redirect,
    url_for, session, current_app, Response, json)
from decorators import login_required
from bson import json_util
from utils import db, send_mail, hash_text, MongoPaginator, get_redis_connection, \
    sensu
import messages
import uuid

bp = admin_blueprint = Blueprint('admin', __name__,
    template_folder='templates')

@bp.route('/')
@login_required
def index():
    return redirect(url_for('admin.events'))

@bp.route('/events/')
@login_required
def events():
    ctx = {
        'events': sensu.get_events(),
    }
    return render_template('admin/events.html', **ctx)

@bp.route('/clients/')
@login_required
def clients():
    ctx = {
        'clients': sensu.get_clients(),
    }
    return render_template('admin/clients.html', **ctx)

@bp.route('/checks/')
@login_required
def checks():
    ctx = {
        'checks': sensu.get_checks(),
    }
    return render_template('admin/checks.html', **ctx)

@bp.route('/stashes/')
@login_required
def stashes():
    ctx = {
        'stashes': sensu.get_stashes(),
    }
    return render_template('admin/stashes.html', **ctx)

@bp.route('/stash/', methods=['POST'])
@login_required
def stash():
    data = json.loads(request.data)
    key = data.get('key', None)
    desc = data.get('description', '')
    if key:
        sensu.create_stash(key, desc)
        flash("{0}: {1}".format(messages.STASH_CREATED, key), 'success')
    return jsonify({'status': 'ok'})

@bp.route('/stash/delete/', methods=['POST'])
@login_required
def delete_stash():
    data = json.loads(request.data)
    key = data.get('key', None)
    if key:
        sensu.delete_stash(key)
        flash(messages.STASH_DELETED, 'success')
    return jsonify({'status': 'ok'})

