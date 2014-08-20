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

"""This code example updates a creative set by adding a companion creative.

To determine which creative sets exist, run get_all_creative_sets.py.

Tags: CreativeSetService.updateCreativeSet
      CreativeSetService.getCreativeSetsByStatement
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

# Set the ID of the creative set to update.
CREATIVE_SET_ID = 'INSERT_CREATIVE_SET_ID_HERE'
COMPANION_CREATIVE_ID = 'INSERT_COMPANION_CREATIVE_ID_HERE'


def main(client, creative_set_id, companion_creative_id):
  # Initialize appropriate service.
  creative_set_service = client.GetService('CreativeSetService',
                                           version='v201408')

  # Create statement to select a single creative set by ID.
  values = [{
      'key': 'creativeSetId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': creative_set_id
      }
  }]
  query = 'WHERE id = :creativeSetId'
  statement = DfpUtils.FilterStatement(query, values)

  # Get creative set.
  response = creative_set_service.GetCreativeSetsByStatement(
      statement.ToStatement())[0]
  creative_sets = response.get('results')

  if creative_sets:
    for creative_set in creative_sets:
      creative_set['companionCreativeIds'].append(companion_creative_id)

    # Update the creative sets on the server.
    creative_sets = creative_set_service.UpdateCreativeSet(creative_sets)[0]

    # Display results.
    for creative_set in creative_sets:
      print (('Creative set with ID \'%s\', master creative ID \'%s\', and '
              'companion creative IDs {%s} was updated.')
             % (creative_set['id'], creative_set['masterCreativeId'],
                ','.join(creative_set['companionCreativeIds'])))
  else:
    print 'No creative sets found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, CREATIVE_SET_ID, COMPANION_CREATIVE_ID)
