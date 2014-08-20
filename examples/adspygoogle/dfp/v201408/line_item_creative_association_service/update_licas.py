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

"""This code example updates the destination URL of all line item creative
associations (LICA).

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


def main(client):
  # Initialize appropriate service.
  lica_service = client.GetService(
      'LineItemCreativeAssociationService', version='v201408')

  # Create statement object to get all LICAs.
  statement = DfpUtils.FilterStatement()

  while True:
    # Get LICAs by statement.
    response = lica_service.GetLineItemCreativeAssociationsByStatement(
        statement.ToStatement())[0]

    licas = response.get('results')

    if licas:
      # Update each local LICA object by changing its destination URL.
      for lica in licas:
        lica['destinationUrl'] = 'http://news.google.com'

      # Update LICAs remotely.
      licas = lica_service.UpdateLineItemCreativeAssociations(licas)

      # Display results.
      for lica in licas:
        print ('LICA with line item id \'%s\', creative id \'%s\', and status '
               '\'%s\' was updated.' % (lica['lineItemId'], lica['creativeId'],
                                        lica['status']))
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  if response['totalResultSetSize'] == 0:
    print 'No LICAs found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
