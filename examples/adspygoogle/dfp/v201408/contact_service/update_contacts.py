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

"""This code example updates contact addresses.

To determine which contacts exist, run get_all_contacts.py.

Tags: ContactService.updateContacts
      ContactService.getContactsByStatement
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

# Set the ID of the contact to update.
CONTACT_ID = 'INSERT_CONTACT_ID_HERE'


def main(client, contact_id):
  # Initialize appropriate service.
  contact_service = client.GetService('ContactService', version='v201408')

  # Create statement object to select the single contact by ID.
  values = [{
      'key': 'id',
      'value': {
          'xsi_type': 'NumberValue',
          'value': contact_id
      }
  }]
  query = 'WHERE id = :id'
  statement = DfpUtils.FilterStatement(query, values, 1)

  # Get contacts by statement.
  response = contact_service.GetContactsByStatement(
      statement.ToStatement())[0]
  contacts = response.get('results')

  if contacts:
    for contact in contacts:
      contact['address'] = '123 New Street, New York, NY, 10011'

    # Update the contact on the server.
    contacts = contact_service.UpdateContacts(contacts)

    # Display results.
    for contact in contacts:
      print (('Contact with ID \'%s\', name \'%s\', and address \'%s\' '
              'was updated.')
             % (contact['id'], contact['name'], contact['address']))
  else:
    print 'No contacts found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, CONTACT_ID)
