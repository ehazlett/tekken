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
from flask import (request, render_template, flash, redirect,
    url_for, session, current_app, Response, json)
from utils import db, hash_text
import utils
from decorators import login_required, admin_required
import messages

bp = accounts_blueprint = Blueprint('accounts', __name__,
    template_folder='templates')

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        u = db.get_user({'username': form.get('username')})
        next_url = utils.get_redirect_target()
        if not next_url:
            next_url = url_for('admin.index')
        if u:
            if hash_text(form.get('password')) == u.get('password'):
                # login
                session['user'] = u
                return redirect(next_url)
            print(u)
        flash(messages.INVALID_USERNAME_PASSWORD, 'error')
        return redirect(url_for('accounts.login'))
    ctx = {}
    return render_template('accounts/login.html', **ctx)

@admin_required
@bp.route('/change-password/', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        form = request.form
        if form.get('password') != form.get('password_confirm'):
            flash(messages.PASSWORDS_NOT_MATCH, 'error')
            return redirect(url_for('accounts.change_password'))
        db.update_user(session.get('user').get('username'), \
            {'password': utils.hash_text(form.get('password'))})
        flash(messages.PASSWORD_UPDATED, 'success')
        return redirect(url_for('admin.index'))
    ctx = {}
    return render_template('accounts/change_password.html', **ctx)

@bp.route('/logout/')
def logout():
    session['user'] = None
    flash(messages.LOGGED_OUT, 'info')
    return redirect(url_for('admin.index'))

