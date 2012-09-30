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
import sys
from flask import Flask
from flask import jsonify
from flask import request
from flask import session
from flask import redirect, render_template, url_for
from flask import g
from utils import db
import getpass
from flask.ext.babel import Babel
from flask.ext.cache import Cache
from flask.ext.pymongo import PyMongo
from flask.ext.mail import Mail
from flask.ext import redis
from datetime import datetime
import config
#from raven.contrib.flask import Sentry
from admin.views import admin_blueprint
from accounts.views import accounts_blueprint

#sentry = Sentry(config.SENTRY_DSN)

app = config.create_app()
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(accounts_blueprint, url_prefix='/accounts')
babel = Babel(app)
cache = Cache(app)
mongo = PyMongo(app)
mail = Mail(app)
redis = redis.init_redis(app)
# add exts for blueprint use
app.config['cache'] = cache
app.config['babel'] = babel
app.config['mongo'] = mongo
app.config['redis'] = redis
app.config['mail'] = mail

# check for admin user
if not db.get_admin({'username': 'admin'}):
    db.create_admin('admin', 'tekken')
    print('Admin user created: username: admin password: tekken')

# ----- context processors
@app.context_processor
def load_user():
    return {'user': session.get('user', None)}

@app.context_processor
def load_sensu_api_url():
    return {'sensu_api_url': app.config.get('SENSU_API_URL')}
# ----- end context processors

# ----- template filters
@app.template_filter('date_from_timestamp')
def date_from_timestamp(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

@app.template_filter('get_user_by_key')
def get_user_by_key(key):
    user = db.get_user({'key': key})
    return user

@app.template_filter('starts_with')
def starts_with(text):
    return False

@app.template_filter('sensu_status_name')
def sensu_status_name(id):
    mapping = {
        1: 'warning',
        2: 'critical',
    }
    return mapping[id]

# ----- end filters

@app.route('/')
def index():
    return redirect(url_for('admin.index'))

# ----- utility functions
def create_admin():
    try:
        username = raw_input('Username: ').strip()
        while True:
            password = getpass.getpass('Password: ')
            password_confirm = getpass.getpass(' (confirm): ')
            if password_confirm == password:
                break
            else:
                print('Passwords do not match... Try again...')
        db.create_admin(username=username, password=password)
        print('Admin created/updated successfully...')
    except KeyboardInterrupt:
        pass

if __name__=='__main__':
    from optparse import OptionParser
    op = OptionParser()
    op.add_option('--host', dest='host', action='store', default='127.0.0.1', \
        help='Hostname/IP on which to listen')
    op.add_option('--port', dest='port', action='store', type=int, \
        default=5000, help='Port on which to listen')
    op.add_option('--create-admin', dest='create_admin', action='store_true', \
        help='Create/Update Admin User')
    opts, args = op.parse_args()

    if opts.create_admin:
        create_admin()
        sys.exit(0)
    app.run(host=opts.host, port=opts.port, debug=True)
