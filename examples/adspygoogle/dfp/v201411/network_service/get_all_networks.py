#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example gets all networks that you have access to with the current login
credentials.

A networkCode should be left out for this request."""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient


def main(client):
  # Initialize appropriate service.
  network_service = client.GetService('NetworkService', version='v201411')

  # Get all networks that you have access to with the current login credentials.
  networks = network_service.GetAllNetworks()

  # Display results.
  for network in networks:
    print ('Network with network code \'%s\' and display name \'%s\' was found.'
           % (network['networkCode'], network['displayName']))

  print '\nNumber of results found: %s' % len(networks)

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
