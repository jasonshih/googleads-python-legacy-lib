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

"""This example deletes a custom targeting key by its name.

To determine which custom targeting keys exist, run
get_all_custom_targeting_keys_and_values.py.

Tags: CustomTargetingService.getCustomTargetingKeysByStatement
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

KEY_NAME = 'INSERT_CUSTOM_TARGETING_KEY_NAME_HERE'


def main(client, key_name):
  # Initialize appropriate service.
  custom_targeting_service = client.GetService(
      'CustomTargetingService', version='v201403')

  values = [{
      'key': 'name',
      'value': {
          'xsi_type': 'TextValue',
          'value': key_name
      }
  }]
  query = 'WHERE name = :name'
  statement = DfpUtils.FilterStatement(query, values)

  deleted_custom_targeting_keys = 0

  # Get custom targeting keys.
  while True:
    response = custom_targeting_service.GetCustomTargetingKeysByStatement(
        statement.ToStatement())[0]
    keys = response.get('results')
    if keys:
      key_ids = [key['id'] for key in keys]
      action = {'type': 'DeleteCustomTargetingKeys'}
      key_query = 'WHERE id IN (%s)' % ', '.join(key_ids)
      key_statement = DfpUtils.FilterStatement(key_query)

      # Delete custom targeting keys.
      result = custom_targeting_service.PerformCustomTargetingKeyAction(
          action, key_statement.ToStatement())[0]

      if result and int(result['numChanges']) > 0:
        deleted_custom_targeting_keys += int(result['numChanges'])
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  if deleted_custom_targeting_keys > 0:
    print ('Number of custom targeting keys deleted: %s'
           % deleted_custom_targeting_keys)
  else:
    print 'No custom targeting keys were deleted.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, KEY_NAME)
