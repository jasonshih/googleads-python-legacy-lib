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

"""This code example updates a single placement to allow for AdSense targeting.

To determine which placements exist, run get_all_placements.py.
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

PLACEMENT_ID = 'INSERT_PLACEMENT_ID_HERE'


def main(client, placement_id):
  # Initialize appropriate service.
  placement_service = client.GetService('PlacementService', version='v201408')
# Create query.
  values = [{
      'key': 'placementId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': placement_id
      }
  }]
  query = 'WHERE id = :placementId'
  statement = DfpUtils.FilterStatement(query, values, 1)

  # Get placements by statement.
  placements = placement_service.GetPlacementsByStatement(
      statement.ToStatement())[0]

  for placement in placements:
    if not placement['targetingDescription']:
      placement['targetingDescription'] = 'Generic description'
    placement['targetingAdLocation'] = 'All images on sports pages.'
    placement['targetingSiteName'] = 'http://code.google.com'
    placement['isAdSenseTargetingEnabled'] = 'true'

  # Update placements remotely.
  placements = placement_service.UpdatePlacements(placements)

  for placement in placements:
    print ('Placement with id \'%s\', name \'%s\', and AdSense targeting '
           'enabled \'%s\' was updated.'
           % (placement['id'], placement['name'],
              placement['isAdSenseTargetingEnabled']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, PLACEMENT_ID)
