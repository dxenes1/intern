﻿# Copyright 2016 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This example shows how to work with the Boss' data model.  The Remote
class methods that being with 'project_' operate on the data model. These
methods are:
    project_list()
    project_create()
    project_get()
    project_update()
    project_delete()

All of these methods take a ndio.ndresource.boss.resource.Resource object, as
a minimum.  The resource object identifies where in the data model hierarchy
the operation should be performed.  For create and update operations, the 
resource object also contains the parameters to place in the database.
"""

from ndio.remote.boss.remote import Remote
from ndio.ndresource.boss.resource import *

rmt = Remote('example.cfg')

API_VER = 'v0.4'

# Turn off SSL cert verification.  This is necessary for interacting with
# developer instances of the Boss.
import requests
from requests import Session
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
rmt.project_service.session_send_opts = { 'verify': False }
rmt.metadata_service.session_send_opts = { 'verify': False }
rmt.volume_service.session_send_opts = { 'verify': False }

# List current collections.
# In general, when performing a list operation, any resource may be used as 
# long as it is the same type.
# For example, to list collections, a CollectionResource without a name (an 
# empty string) may be used.
coll = CollectionResource('', API_VER)
coll_list = rmt.project_list(coll)

# For resources below the collection level, the parents must be specified.
# For example to list all the channels that are part of the gray collection 
# and alpha experiment:
channels = ChannelResource('', 'gray', 'alpha', API_VER)
chan_list = rmt.project_list(channels)
for chan in chan_list:
    print(chan['name'])

# When creating a new resource, the corresponding resource object will need
# the required attributes populated.
# For example, to add a channel named beta to the alpha experiment referenced
# in the previous example:
betaChan = ChannelResource('beta', 'gray', 'alpha', API_VER, 'test channel')
newBetaChan = rmt.project_create(betaChan)

# Note that the create method returns a new instance of the ChannelResource.
# This new instance is populated with additional information, such as the id
# used by the Boss API.  The new instance also has its `raw` attribute populated
# with all the JSON data returned by the Boss API.
if not newBetaChan:
    print('Creating {} channel failed.'.format(betaChan.name))

# Display raw channel data from the Boss API:
print(newBetaChan.raw)

# We forgot, to set the channel's data type to uint16.  Let's fix that by
# updating the channel.
betaChan.datatype = 'uint16'
if not rmt.project_update(betaChan.name, betaChan):
    print('Updating {} channel failed.'.format(betaChan.name))

# Let's get the channel and verify the data type was updated.
chan_data = rmt.project_get(betaChan)
print(chan_data['datatype'])

# To demonstrate the final method available for project operations, we will
# delete the beta channel.
if not rmt.project_delete(betaChan):
    print('Delete {} channel failed.'.format(betaChan.name))

chan_list = rmt.project_list(channels)
for chan in chan_list:
    print(chan['name'])