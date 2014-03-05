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

"""This code example deactivates all LICAs for the line item.

To determine which LICAs exist, run get_all_licas.py."""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils

# Set the id of the line item in which to deactivate LICAs.
LINE_ITEM_ID = 'INSERT_LINE_ITEM_ID_HERE'


def main(client, line_item_id):
  # Initialize appropriate service.
  lica_service = client.GetService(
      'LineItemCreativeAssociationService', version='v201403')

  # Create query.
  values = [{
      'key': 'lineItemId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': line_item_id
      }
  }, {
      'key': 'status',
      'value': {
          'xsi_type': 'TextValue',
          'value': 'ACTIVE'
      }
  }]
  query = 'WHERE lineItemId = :lineItemId AND status = :status'
  statement = DfpUtils.FilterStatement(query, values)

  num_deactivated_licas = 0

  # Get LICAs by statement.
  while True:
    response = lica_service.GetLineItemCreativeAssociationsByStatement(
        statement.ToStatement())[0]
    licas = response.get('results')
    if licas:
      for lica in licas:
        for lica in licas:
          print ('LICA with line item id \'%s\', creative id \'%s\', and status'
                 ' \'%s\' will be deactivated.' %
                 (lica['lineItemId'], lica['creativeId'], lica['status']))

      # Perform action.
      result = lica_service.PerformLineItemCreativeAssociationAction(
          {'type': 'DeactivateLineItemCreativeAssociations'},
          statement.ToStatement())[0]
      if result and int(result['numChanges']) > 0:
        num_deactivated_licas += int(result['numChanges'])
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  # Display results.
  if num_deactivated_licas > 0:
    print 'Number of LICAs deactivated: %s' % num_deactivated_licas
  else:
    print 'No LICAs were deactivated.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, LINE_ITEM_ID)
