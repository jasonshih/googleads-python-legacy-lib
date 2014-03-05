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

"""This code example updates company comments.

To determine which companies exist, run get_all_companies.py.

Tags: CompanyService.updateCompanies
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

# Set the ID of the company to update.
COMPANY_ID = 'INSERT_COMPANY_ID_HERE'


def main(client, company_id):
  # Initialize appropriate service.
  company_service = client.GetService('CompanyService', version='v201403')

  # Create statement object to only select a single company by ID.
  values = [{
      'key': 'id',
      'value': {
          'xsi_type': 'NumberValue',
          'value': company_id
      }
  }]
  query = 'WHERE id = :id'
  statement = DfpUtils.FilterStatement(query, values, 1)

  # Get companies by statement.
  response = company_service.GetCompaniesByStatement(
      statement.ToStatement())[0]
  companies = response.get('results')
  if companies:
    # Display results.
    for company in companies:
      company['comment'] += ' Updated.'

    # Update the companies on the server.
    companies = company_service.UpdateCompanies(companies)

    # Display results.
    for company in companies:
      print (('Company with ID \'%s\', name \'%s\', and comment \'%s\''
              'was updated.')
             % (company['id'], company['name'], company['comment']))
  else:
    print 'No companies found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, COMPANY_ID)
