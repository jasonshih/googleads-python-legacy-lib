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

"""This example removes the user from all its teams.

To determine which users exist, run get_all_users.py.

Tags: UserTeamAssociationService.performUserTeamAssociationAction
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

USER_ID = 'INSERT_USER_ID_HERE'


def main(client, user_id):
  # Initialize appropriate service.
  user_team_association_service = client.GetService(
      'UserTeamAssociationService', version='v201411')

  # Create filter text to select user team associations by the user ID.
  values = [{
      'key': 'userId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': user_id
      }
  }]
  query = 'WHERE userId = :userId'

  # Create a filter statement.
  statement = DfpUtils.FilterStatement(query, values)

  # Get user team associations by statement.
  response = user_team_association_service.GetUserTeamAssociationsByStatement(
      statement.ToStatement())[0]
  user_team_associations = response.get('results')

  for user_team_association in user_team_associations:
    print ('User team association between user with ID \'%s\' and team with '
           'ID \'%s\' will be deleted.' % (user_team_association['userId'],
                                           user_team_association['teamId']))
  print ('Number of teams that the user will be removed from: %s' %
         len(user_team_associations))

  # Perform action.
  result = user_team_association_service.PerformUserTeamAssociationAction(
      {'type': 'DeleteUserTeamAssociations'},
      {'query': query, 'values': values})[0]

  # Display results.
  if result and int(result['numChanges']) > 0:
    print ('Number of teams that the user was removed from: %s'
           % result['numChanges'])
  else:
    print 'No user team associations were deleted.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, USER_ID)
