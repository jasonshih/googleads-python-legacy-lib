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

"""This example gets custom targeting values for the given predefined custom
targeting key.

To create custom targeting values, run
create_custom_targeting_keys_and_values.py. To determine which custom
targeting keys exist, run get_all_custom_targeting_keys_and_values.py."""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils

CUSTOM_TARGETING_KEY_ID = 'INSERT_CUSTOM_TARGETING_KEY_ID_HERE'


def main(client, key_id):
  # Initialize appropriate service.
  custom_targeting_service = client.GetService(
      'CustomTargetingService', version='v201411')

  values = [{
      'key': 'keyId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': key_id
      }
  }]
  query = 'WHERE customTargetingKeyId = :keyId'
  statement = DfpUtils.FilterStatement(query, values)

  # Get custom targeting values by statement.
  while True:
    response = custom_targeting_service.GetCustomTargetingValuesByStatement(
        statement.ToStatement())[0]
    values = response.get('results')
    if values:
      # Display results.
      for value in values:
        print ('Custom targeting value with id \'%s\', name \'%s\', and display'
               ' name \'%s\' was found.'
               % (value['id'], value['name'], value['displayName']))
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  print '\nNumber of results found: %s' % response['totalResultSetSize']

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, CUSTOM_TARGETING_KEY_ID)
