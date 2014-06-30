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

"""This example updates custom field descriptions.

To determine which custom fields exist, run get_all_custom_fields.py.

Tags: CustomFieldService.updateCustomFields
      CustomFieldService.getCustomFieldByStatement
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

# Set the ID of the custom field to update.
CUSTOM_FIELD_ID = 'INSERT_CUSTOM_FIELD_ID_HERE'


def main(client, custom_field_id):
  # Initialize appropriate service.
  custom_field_service = client.GetService(
      'CustomFieldService', version='v201405')

  # Create statement to get a custom field.
  values = [{
      'key': 'customFieldId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': custom_field_id
      }
  }]
  query = 'WHERE id = :customFieldId'
  statement = DfpUtils.FilterStatement(query, values)

  # Get custom field.
  custom_fields = custom_field_service.GetCustomsFieldByStatement(
      statement.ToStatement())[0]

  if custom_fields:
    for custom_field in custom_fields:
      custom_field['description'] += ' Updated.'

    # Update the custom field on the server.
    custom_fields = custom_field_service.UpdateCustomFields(custom_fields)

    # Display results.
    for custom_field in custom_fields:
      print (('Custom field with ID \'%s\', name \'%s\', and '
              'description \'%s\' was updated.')
             % (custom_field['id'], custom_field['name'],
                custom_field['description']))
  else:
    print 'No custom fields found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, CUSTOM_FIELD_ID)
