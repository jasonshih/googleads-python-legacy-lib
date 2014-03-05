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

"""This example gets all predefined custom targeting keys.

To create custom targeting keys, run create_custom_targeting_keys_and_values.py.
"""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils


def main(client):
  # Initialize appropriate service.
  custom_targeting_service = client.GetService(
      'CustomTargetingService', version='v201403')

  values = [{
      'key': 'type',
      'value': {
          'xsi_type': 'TextValue',
          'value': 'PREDEFINED'
      }
  }]
  query = 'WHERE type = :type',
  statement = DfpUtils.FilterStatement(query, values)

  # Get custom targeting keys by statement.
  while True:
    response = custom_targeting_service.GetCustomTargetingKeysByStatement(
        statement.ToStatement())[0]
    keys = response.get('results')
    if keys:
      # Display results.
      for key in keys:
        print ('Custom targeting key with id \'%s\', name \'%s\', display name '
               '\'%s\', and type \'%s\' was found.'
               % (key['id'], key['name'], key['displayName'], key['type']))
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  print '\nNumber of results found: %s' % response['totalResultSetSize']

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
