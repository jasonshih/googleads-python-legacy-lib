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

"""This code example archives ad units.

The parent ad unit and all ad units underneath it will be archived. To create ad
units, run create_ad_units.py.

Tags: InventoryService.getAdUnitsByStatement
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

PARENT_AD_UNIT_ID = 'INSERT_AD_UNIT_ID_HERE'


def main(client, parent_id):
  # Initialize appropriate service.
  inventory_service = client.GetService('InventoryService', version='v201408')

  # Create a query to select ad units under the parent ad unit and the parent ad
  # unit.
  values = [{
      'key': 'parentId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': parent_id
      }
  }]
  query = 'WHERE parentId = :parentId or id = :parentId'
  statement = DfpUtils.FilterStatement(query, values)

  ad_units_archived = 0

  # Get ad units by statement.
  while True:
    response = inventory_service.GetAdUnitsByStatement(
        statement.ToStatement())[0]
    ad_units = response.get('results')
    if ad_units:
      for ad_unit in ad_units:
        print ('Ad unit with ID \'%s\' and name \'%s\' will be archived.'
               % (ad_unit['id'], ad_unit['name']))
      # Perform action.
      result = inventory_service.PerformAdUnitAction(
          {'type': 'ArchiveAdUnits'}, statement.ToStatement())[0]
      if result and int(result['numChanges']) > 0:
        ad_units_archived += int(result['numChanges'])
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  # Display results.
  if ad_units_archived > 0:
    print 'Number of ad units archived: %s' % ad_units_archived
  else:
    print 'No ad units were archived.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, PARENT_AD_UNIT_ID)
