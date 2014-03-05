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

"""This code example gets all creatives.

To create creatives, run create_creatives.py.

Tags: CreativeService.getCreativesByStatement
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
  creative_service = client.GetService('CreativeService', version='v201311')

  # Create statement object to select all creatives.
  statement = DfpUtils.FilterStatement()

  # Get creatives by statement.
  while True:
    response = creative_service.GetCreativesByStatement(
        statement.ToStatement())[0]
    creatives = response.get('results')
    if creatives:
      # Display results.
      for creative in creatives:
        print ('Creative with id \'%s\', name \'%s\', and type \'%s\' was '
               'found.' % (creative['id'], creative['name'],
                           creative['Creative_Type']))
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  print '\nNumber of results found: %s' % response['totalResultSetSize']

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
