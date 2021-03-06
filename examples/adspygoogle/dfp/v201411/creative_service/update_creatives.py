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

"""This code example updates the destination URL of a single image creative.

To determine which image creatives exist, run get_all_creatives.py.

Tags: CreativeService.updateCreatives
      CreativeService.getCreativesByStatement
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

IMAGE_CREATIVE_ID = 'INSERT_IMAGE_CREATIVE_ID_HERE'


def main(client, image_creative_id):
  # Initialize appropriate service.
  creative_service = client.GetService('CreativeService', version='v201411')

  # Create statement object to get all image creatives.
  values = [{
      'key': 'type',
      'value': {
          'xsi_type': 'TextValue',
          'value': 'ImageCreative'
      }
  }, {
      'key': 'id',
      'value': {
          'xsi_type': 'NumberValue',
          'value': image_creative_id
      }
  }]
  query = 'WHERE creativeType = :type AND id = :id'
  statement = DfpUtils.FilterStatement(query, values, 1)

  # Get creatives by statement.
  response = creative_service.GetCreativesByStatement(
      statement.ToStatement())[0]
  creatives = response.get('results')

  if creatives:
    # Update each local creative object by changing its destination URL.
    for creative in creatives:
      creative['destinationUrl'] = 'http://news.google.com'

    # Update creatives remotely.
    creatives = creative_service.UpdateCreatives(creatives)

    # Display results.
    for creative in creatives:
      print ('Image creative with id \'%s\' and destination URL \'%s\' was '
             'updated.' % (creative['id'], creative['destinationUrl']))
  else:
    print 'No creatives found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, IMAGE_CREATIVE_ID)
