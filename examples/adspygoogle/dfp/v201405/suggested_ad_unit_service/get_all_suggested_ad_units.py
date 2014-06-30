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

"""This code example gets all suggested ad units.

To approve suggested ad units, run approve_suggested_ad_units.py. This feature
is only available to DFP premium solution networks.
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
  suggested_ad_unit_service = client.GetService(
      'SuggestedAdUnitService', version='v201405')

  # Create a filter statement.
  statement = DfpUtils.FilterStatement()

  # Get suggested ad units by statement.
  while True:
    response = suggested_ad_unit_service.GetSuggestedAdUnitsByStatement(
        statement.ToStatement())[0]
    suggested_ad_units = response.get('results')
    if suggested_ad_units:
      # Display results.
      for suggested_ad_unit in suggested_ad_units:
        print ('Ad unit with id \'%s\' and number of requests \'%s\' was found.'
               % (suggested_ad_unit['id'], suggested_ad_unit['numRequests']))
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  print '\nNumber of results found: %s' % response['totalResultSetSize']

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
