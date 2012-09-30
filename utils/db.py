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
from flask import current_app
from uuid import uuid4
from utils import hash_text, get_mongo_connection

def create_user(username=None, first_name=None, last_name=None):
    """
    Creates a new user

    :param username: Username of user
    :param first_name: First name of user
    :param last_name: Last name of user

    """
    mongo = get_mongo_connection()
    obj_id = mongo.db.accounts.save({
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'api_key': str(uuid4()), # TEMPORARY ? generate initial api key
        'puppet_master': current_app.config.get('PUPPET_MASTER_HOST'),
        'key': str(uuid4()),
    }, safe=True)
    return mongo.db.accounts.find_one(obj_id)

def create_admin(username=None, password=None):
    """
    Creates a new admin

    :param username: Username of user
    :param password: Password of user

    """
    mongo = get_mongo_connection()
    obj_id = mongo.db.admins.save({
        'username': username,
        'password': hash_text(password),
        'is_admin': True,
    }, safe=True)
    return mongo.db.admins.find_one(obj_id)

def get_admin(data={}):
    """
    Returns an admin object from the datastore

    :param data: Data to use for query

    """
    mongo = get_mongo_connection()
    user = mongo.db.admins.find_one(data)
    return user

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

def create_node(node_name=None, key=None):
    """
    Creates a new node

    :param node_name: Name of node
    :param key: Account key of which node belogs

    """
    mongo = get_mongo_connection()
    node = mongo.db.nodes.find_one({'node_name': node_name, 'key': key})
    if node:
        return node
    obj_id = mongo.db.nodes.save({
        'node_name': node_name,
        'key': key,
        'modules': ['arcus'],
    }, safe=True)
    return mongo.db.nodes.find_one(obj_id)

def get_node(node_name=None, key=None):
    """
    Returns a node

    :param node_name: Name of node
    :param key: (optional) Account key of which node belongs

    """
    mongo = get_mongo_connection()
    data = {'node_name': node_name}
    if key:
        data['key'] = key
    node = mongo.db.nodes.find_one(data)
    return node

def get_nodes(limit=0, skip=0):
    """
    Returns all nodes

    :param limit: Limit number of returned nodes
    :param skip: Start returning nodes at skip
    :returns: List of objects

    """
    mongo = get_mongo_connection()
    return mongo.db.nodes.find().skip(skip).limit(limit)

def delete_node(node_name=None, key=None):
    """
    Deletes a node

    :param node_name: Name of node to delete
    :param key: Key of account of which node belongs

    """
    mongo = get_mongo_connection()
    return mongo.db.nodes.remove({'node_name': node_name, 'key': key})

def update_node_modules(node_name=None, key=None, action=None, modules=[]):
    mongo = get_mongo_connection()
    node = mongo.db.nodes.find_one({'node_name': node_name, 'key': key})
    if action:
        action = action.lower()
    # always leave the arcus module
    if 'arcus' in modules and action == 'remove':
        modules.pop(modules.index('arcus'))
    # de-dupe existing
    if action == 'add':
        [modules.pop(modules.index(x)) for x in node.get('modules') if x in modules]
    op = {
        'add': '$pushAll',
        'remove': '$pullAll',
    }
    mongo.db.nodes.update({'node_name': node_name, 'key': key}, { op[action]: {'modules': modules} })
    return mongo.db.nodes.find_one({'node_name': node_name, 'key': key})
