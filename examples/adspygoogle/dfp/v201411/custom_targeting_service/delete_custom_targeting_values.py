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

"""This example deletes custom targeting values for a given custom targeting
key.

To determine which custom targeting keys and values exist, run
get_all_custom_targeting_keys_and_values.py.

Tags: CustomTargetingService.getCustomTargetingValuesByStatement
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

KEY_ID = 'INSERT_CUSTOM_TARGETING_KEY_ID_HERE'


def main(client, key_id):
  # Initialize appropriate service.
  custom_targeting_service = client.GetService(
      'CustomTargetingService', version='v201411')

  filter_values = [{
      'key': 'keyId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': key_id
      }
  }]
  query = 'WHERE customTargetingKeyId = :keyId'
  statement = DfpUtils.FilterStatement(query, filter_values)

  deleted_custom_targeting_values = 0

  # Get custom targeting values.
  while True:
    response = custom_targeting_service.GetCustomTargetingValuesByStatement(
        statement.ToStatement())[0]
    values = response.get('results')
    if values:
      value_ids = [value['id'] for value in values]
      action = {'type': 'DeleteCustomTargetingValues'}
      value_query = ('WHERE customTargetingKeyId = :keyId '
                     'AND id IN (%s)' % ', '.join(value_ids))
      value_statement = DfpUtils.FilterStatement(value_query, filter_values)

      # Delete custom targeting values.
      result = custom_targeting_service.PerformCustomTargetingValueAction(
          action, value_statement.ToStatement())[0]
      if result and int(result['numChanges']) > 0:
        deleted_custom_targeting_values += int(result['numChanges'])
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  if deleted_custom_targeting_values > 0:
    print ('Number of custom targeting values deleted: %s'
           % deleted_custom_targeting_values)
  else:
    print 'No custom targeting values were deleted.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, KEY_ID)
