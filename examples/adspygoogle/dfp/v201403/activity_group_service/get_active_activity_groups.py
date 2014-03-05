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

"""This code example gets all active activity groups.

To create activity groups, run create_activity_groups.py.

Tags: ActivityGroupService.getActivityGroupsByStatement
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
  activity_group_service = client.GetService('ActivityGroupService',
                                             version='v201403')

  # Create statement object to only select active activity groups.
  values = [{
      'key': 'status',
      'value': {
          'xsi_type': 'TextValue',
          'value': 'ACTIVE'
      }
  }]
  query = 'WHERE status = :status'

  # Create a filter statement.
  statement = DfpUtils.FilterStatement(query, values)

  # Get activity groups by statement.
  while True:
    response = activity_group_service.GetActivityGroupsByStatement(
        statement.ToStatement())[0]
    activity_groups = response.get('results')
    if activity_groups:
      # Display results.
      for activity_group in activity_groups:
        print ('Activity group with ID \'%s\' and name \'%s\' was found.'
               % (activity_group['id'], activity_group['name']))
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  print '\nNumber of results found: %s' % response['totalResultSetSize']

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
