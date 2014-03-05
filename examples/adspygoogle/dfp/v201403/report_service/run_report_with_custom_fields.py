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

"""This code example runs a report that with custom fields found in the line
items of an order.
"""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))
import tempfile
import time

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils

# Set the ID of the order to get line items from.
ORDER_ID = 'INSERT_ORDER_ID_HERE'


def main(client, order_id):
  # Initialize appropriate services.
  line_item_service = client.GetService('LineItemService', version='v201403')
  report_service = client.GetService('ReportService', version='v201403')

  # Filter for line items of a given order.
  values = [{
      'key': 'orderId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': order_id
      }
  }]
  query = 'WHERE orderId = :orderId'

  # Create a filter statement.
  statement = DfpUtils.FilterStatement(query, values)

  # Collect all line item custom field IDs for an order.
  custom_field_ids = set()

  # Get users by statement.
  while True:
    response = line_item_service.GetLineItemsByStatement(
        statement.ToStatement())[0]
    line_items = response.get('results')
    if line_items:
      # Get custom field IDs from the line items of an order.
      for line_item in line_items:
        if 'customFieldValues' in line_item:
          for custom_field_value in line_item['customFieldValues']:
            custom_field_ids.add(custom_field_value['customFieldId'])
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  # Create statement object to filter for an order.
  filter_statement = {'query': query, 'values': values}

  # Create report job.
  report_job = {
      'reportQuery': {
          'dimensions': ['LINE_ITEM_ID', 'LINE_ITEM_NAME'],
          'statement': filter_statement,
          'columns': ['AD_SERVER_IMPRESSIONS'],
          'dateRangeType': 'LAST_MONTH',
          'customFieldIds': list(custom_field_ids)
      }
  }

  # Run report.
  report_job = report_service.RunReportJob(report_job)[0]

  # Wait for report to complete.
  status = report_job['reportJobStatus']
  while status != 'COMPLETED' and status != 'FAILED':
    print 'Report job with \'%s\' id is still running.' % report_job['id']
    time.sleep(30)
    status = report_service.GetReportJob(report_job['id'])[0]['reportJobStatus']

  if status == 'FAILED':
    print ('Report job with id \'%s\' failed to complete successfully.'
           % report_job['id'])
  else:
    # Change to your preferred export format.
    export_format = 'CSV_DUMP'

    report_file = tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=False)

    # Download report data.
    DfpUtils.DownloadReportToFile(
        report_job['id'], export_format, report_service, report_file)

    report_file.close()

    # Display results.
    print 'Report job with id \'%s\' downloaded to:\n%s' % (
        report_job['id'], report_file.name)

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, ORDER_ID)
