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

"""This example gets all custom targeting keys and the values.

To create custom targeting keys and values, run
create_custom_targeting_keys_and_values.py."""

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
      'CustomTargetingService', version='v201405')

  # Create statement to get all targeting keys.
  targeting_key_statement = DfpUtils.FilterStatement()

  all_keys = []

  # Get custom targeting keys by statement.
  while True:
    response = custom_targeting_service.GetCustomTargetingKeysByStatement(
        targeting_key_statement.ToStatement())[0]
    keys = response.get('results')
    if keys:
      all_keys.extend(keys)
      targeting_key_statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  if all_keys:
    # Create map of custom targeting key id to custom targeting values.
    key_value_map = {}

    # Create statement to get all targeting values.
    query = ('WHERE customTargetingKeyId IN (%s)'
             % ', '.join([key['id'] for key in all_keys]))
    targeting_value_statement = DfpUtils.FilterStatement(query)

    # Get custom targeting values by statement.
    while True:
      response = custom_targeting_service.GetCustomTargetingValuesByStatement(
          targeting_value_statement.ToStatement())[0]
      values = response.get('results')
      if values:
        for key in all_keys:
          for value in values:
            if key['id'] == value['customTargetingKeyId']:
              if key['id'] not in key_value_map.keys():
                key_value_map[key['id']] = []
              key_value_map[key['id']].append(value)
        targeting_value_statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
      else:
        break

    # Display results.
    for key in all_keys:
      print ('Custom targeting key with id \'%s\', name \'%s\', display name '
             '\'%s\', and type \'%s\' was found.'
             %(key['id'], key['name'], key['displayName'], key['type']))
      if key['id'] in key_value_map.keys():
        for value in key_value_map[key['id']]:
          print ('\tCustom targeting value with id \'%s\', name \'%s\', and '
                 'display name \'%s\' was found.'
                 % (value['id'], value['name'], value['displayName']))
  else:
    print 'No keys were found.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)

