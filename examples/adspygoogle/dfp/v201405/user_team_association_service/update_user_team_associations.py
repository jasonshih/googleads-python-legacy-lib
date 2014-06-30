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

"""This example updates user team associations.

It updates a user team association by setting the overridden access type to read
only for all teams that the user belongs to. To determine which users exists,
run get_all_users.py.

Tags: UserTeamAssociationService.getUserTeamAssociationsByStatement
Tags: UserTeamAssociationService.updateUserTeamAssociations
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

USER_ID = 'INSERT_USER_ID_TO_UPDATE_HERE'


def main(client, user_id):
  # Initialize appropriate service.
  user_team_association_service = client.GetService(
      'UserTeamAssociationService', version='v201405')

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

  if user_team_associations:
    # Update each local user team association to read only access.
    for user_team_association in user_team_associations:
      user_team_association['overriddenTeamAccessType'] = 'READ_ONLY'

    # Update user team associations on the server.
    user_team_associations = (
        user_team_association_service.UpdateUserTeamAssociations(
            user_team_associations))

    # Display results.
    if user_team_associations:
      for user_team_association in user_team_associations:
        print ('User team association between user with ID \'%s\' and team with'
               ' ID \'%s\' was updated.' % (user_team_association['userId'],
                                            user_team_association['teamId']))
    else:
      print 'No user team associations were updated.'
  else:
    print 'No user team associations found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, USER_ID)
