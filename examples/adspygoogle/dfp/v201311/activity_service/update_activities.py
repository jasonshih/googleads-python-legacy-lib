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

"""This code example updates activities.

To determine which activities exist, run get_all_activities.py.

Tags: ActivityService.updateActivities
      ActivityService.getActivitiesByStatement
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

# Set the ID of the activity to update.
ACTIVITY_ID = 'INSERT_ACTIVITY_ID_HERE'


def main(client, activity_id):
  # Initialize appropriate service.
  activity_service = client.GetService('ActivityService', version='v201311')

  # Create statement object to select one activity by ID to update.
  values = [{
      'key': 'activityId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': activity_id
      }
  }]
  query = 'WHERE id = :activityId'
  statement = DfpUtils.FilterStatement(query, values, 1)

  # Get activities by statement.
  response = activity_service.GetActivitiesByStatement(
      statement.ToStatement())[0]
  activities = response.get('results')
  if activities:
    for activity in activities:
      # Update the expected URL.
      activity['expectedURL'] = 'https://google.com'
    # Update the activity on the server.
    activities = activity_service.UpdateActivities(activities)

    for updated_activity in activities:
      print (('Activity with ID \'%s\' and name \'%s\' was updated.')
             % (updated_activity['id'], updated_activity['name']))
  else:
    print 'No activities found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, ACTIVITY_ID)
