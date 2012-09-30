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
from utils import hash_text, get_mongo_connection

def create_user(username=None, password=None, first_name=None, last_name=None, \
    is_admin=False):
    """
    Creates a new user

    :param username: Username of user
    :param password: User password
    :param first_name: First name of user
    :param last_name: Last name of user
    :param is_admin: Admin user

    """
    mongo = get_mongo_connection()
    obj_id = mongo.db.accounts.save({
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'password': hash_text(password),
        'is_admin': True,
    }, safe=True)
    return mongo.db.accounts.find_one(obj_id)

def get_user(data={}):
    """
    Returns a user object from the datastore

    :param data: Data to use for query

    """
    mongo = get_mongo_connection()
    user = mongo.db.accounts.find_one(data)
    return user

def update_user(username=None, data={}):
    """
    Updates a user with the specified data

    :param username: Username to update
    :param data: Data to update as a dict

    """
    mongo = get_mongo_connection()
    return mongo.db.accounts.update({'username': username}, {'$set': data })

def delete_user(username=None):
    """
    Deletes a user

    :param username: Username to delete

    """
    mongo = get_mongo_connection()
    return mongo.db.accounts.remove({'username': username}, safe=True)

