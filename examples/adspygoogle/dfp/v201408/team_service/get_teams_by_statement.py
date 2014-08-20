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

"""This example gets a single team by ID.

To create teams, run create_teams.py.

Tags: TeamService.getTeamsByStatement
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

TEAM_ID = 'INSERT_TEAM_ID_HERE'


def main(client, team_id):
  # Initialize appropriate service.
  team_service = client.GetService('TeamService', version='v201408')

  # Create a filter statement to select a single team by ID.
  values = [{
      'key': 'teamId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': team_id
      }
  }]
  query = 'WHERE id = :teamId'
  statement = DfpUtils.FilterStatement(query, values)

  while True:
    # Get teams by statement.
    response = team_service.GetTeamsByStatement(statement.ToStatement())[0]
    teams = response.get('results')
    if teams:
      # Display results.
      for team in teams:
        print ('Team with id \'%s\' and name \'%s\' was found.'
               % (team['id'], team['name']))
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  print '\nNumber of results found: %s' % response['totalResultSetSize']

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, TEAM_ID)
