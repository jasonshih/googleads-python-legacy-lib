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

"""This code example approves all eligible draft and pending orders.

To determine which orders exist, run get_all_orders.py."""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import datetime
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils


def main(client):
  # Initialize appropriate service.
  order_service = client.GetService('OrderService', version='v201408')

  # Create query.
  values = [{
      'key': 'today',
      'value': {
          'xsi_type': 'TextValue',
          'value': datetime.date.today().strftime('%Y-%m-%dT%H:%M:%S')
      }
  }]
  query = ('WHERE status in (\'DRAFT\', \'PENDING_APPROVAL\')'
           ' AND endDateTime >= :today AND isArchived = FALSE')

  # Create a filter statement.
  statement = DfpUtils.FilterStatement(query, values)
  orders_approved = 0

  # Get orders by statement.
  while True:
    response = order_service.GetOrdersByStatement(statement.ToStatement())[0]
    orders = response.get('results')
    if orders:
      # Display results.
      for order in orders:
        print ('Order with id \'%s\', name \'%s\', and status \'%s\' will be '
               'approved.' % (order['id'], order['name'], order['status']))
      # Perform action.
      result = order_service.PerformOrderAction(
          {'type': 'ApproveOrders'}, statement.ToStatement())[0]
      if result and int(result['numChanges']) > 0:
        orders_approved += int(result['numChanges'])
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  # Display results.
  if orders_approved > 0:
    print 'Number of orders approved: %s' % orders_approved
  else:
    print 'No orders were approved.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
