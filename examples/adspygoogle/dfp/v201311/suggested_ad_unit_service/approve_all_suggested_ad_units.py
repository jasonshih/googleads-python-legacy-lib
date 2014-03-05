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

"""This code example approves all suggested ad units with 50 or more requests.

This feature is only available to DFP premium solution networks.
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

THRESHOLD_NUMBER_OF_REQUESTS = '50'


def main(client):
    # Initialize appropriate service.
  suggested_ad_unit_service = client.GetService(
      'SuggestedAdUnitService', version='v201311')

  values = [{
      'key': 'numRequests',
      'value': {
          'xsi_type': 'NumberValue',
          'value': THRESHOLD_NUMBER_OF_REQUESTS
      }
  }]

  query = 'WHERE numRequests > :numRequests'

  # Create a filter statement.
  statement = DfpUtils.FilterStatement(query, values)
  num_approved_suggested_ad_units = 0

  # Get suggested ad units by statement.
  while True:
    response = suggested_ad_unit_service.GetSuggestedAdUnitsByStatement(
        statement.ToStatement())[0]
    suggested_ad_units = response.get('results')
    if suggested_ad_units:
      # Print suggested ad units that will be approved.
      for suggested_ad_unit in suggested_ad_units:
        print ('Suggested ad unit with id \'%s\', and number of requests \'%s\''
               ' will be approved.' % (suggested_ad_unit['id'],
                                       suggested_ad_unit['numRequests']))

      # Approve suggested ad units.
      result = suggested_ad_unit_service.performSuggestedAdUnitAction(
          {'type': 'ApproveSuggestedAdUnit'},
          statement.ToStatement())[0]
      if result and int(result['numChanges']) > 0:
        num_approved_suggested_ad_units += int(result['numChanges'])
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  if num_approved_suggested_ad_units > 0:
    print ('Number of suggested ad units approved: %s' %
           num_approved_suggested_ad_units)
  else:
    print 'No suggested ad units were approved.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)

