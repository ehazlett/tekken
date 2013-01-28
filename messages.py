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
from flaskext.babel import gettext

ACCESS_DENIED = gettext('Access denied')
CLIENT_DELETED = gettext('Client deleted.  It may take a moment to refresh.')
ERROR_CREATING_USER = gettext('There was an error creating the account.')
EVENT_RESOLVED = gettext('Event resolved.')
EXISTING_USER = gettext('There is already a user registered with that username.')
INVALID_USERNAME_PASSWORD = gettext('Invalid or unspecified username or password')
LOGGED_OUT = gettext('You are now logged out')
MISSING_USERNAME_OR_PASSWORD = gettext('Missing username or password')
PASSWORDS_NOT_MATCH = gettext('Passwords do not match')
PASSWORD_UPDATED = gettext('Password updated')
STASH_CREATED = gettext('Stash created')
STASH_DELETED = gettext('Stash deleted')
UNKNOWN_NODE = gettext('Unknown node specified')
USER_CREATED = gettext('User created')
