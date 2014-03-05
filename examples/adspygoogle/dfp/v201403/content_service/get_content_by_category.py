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

"""This code example gets all active content categorized as a "comedy" using the
network's content browse custom targeting key.

This feature is only available to DFP video publishers.

Tags: ContentService.getContentByStatement
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
  content_service = client.GetService('ContentService', version='v201403')
  network_service = client.GetService('NetworkService', version='v201403')
  custom_targeting_service = client.GetService(
      'CustomTargetingService', version='v201403')

  # Get the network's content browse custom targeting key.
  network = network_service.GetCurrentNetwork()[0]
  key_id = network['contentBrowseCustomTargetingKeyId']

  # Create a statement to select the categories matching the name comedy.
  values = [
      {
          'key': 'contentBrowseCustomTargetingKeyId',
          'value': {
              'xsi_type': 'NumberValue',
              'value': key_id
          }
      },
      {
          'key': 'category',
          'value': {
              'xsi_type': 'TextValue',
              'value': 'comedy'
          }
      }
  ]
  category_filter_query = ('WHERE customTargetingKeyId = '
                           ':contentBrowseCustomTargetingKeyId and name = '
                           ':category')
  category_filter_statement = DfpUtils.FilterStatement(
      category_filter_query, values, 1)

  # Get categories matching the filter statement.
  response = custom_targeting_service.GetCustomTargetingValuesByStatement(
      category_filter_statement.ToStatement())[0]

  # Get the custom targeting value ID for the comedy category.
  category_custom_targeting_value = response.get('results')
  if category_custom_targeting_value:
    category_custom_targeting_value_id = (
        category_custom_targeting_value[0]['id'])

    # Create a statement to select the active content.
    content_values = [
        {
            'key': 'status',
            'value': {
                'xsi_type': 'TextValue',
                'value': 'ACTIVE'
            }
        }
    ]
    content_query = 'WHERE status = :status'
    content_statement = DfpUtils.FilterStatement(content_query, content_values)

    while True:
      # Get the content by statement and custom targeting value.
      response = content_service.GetContentByStatementAndCustomTargetingValue(
          content_statement.ToStatement(),
          category_custom_targeting_value_id)[0]
      content = response.get('results')
      if content:
        # Display results.
        for content_item in content:
          print ('Content with id \'%s\', name \'%s\', and status \'%s\' was '
                 'found.' % (content_item['id'], content_item['name'],
                             content_item['status']))
        content_statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
      else:
        break

    print '\nNumber of results found: %s' % response['totalResultSetSize']

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
