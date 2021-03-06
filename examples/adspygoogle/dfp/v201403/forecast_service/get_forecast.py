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

"""This code example gets a forecast for a prospective line item.

To determine which placements exist, run get_all_placements.py."""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
from datetime import date
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient

# Set the placement that the prospective line item will target.
TARGET_PLACEMENT_IDS = ['INSERT_PLACEMENT_IDS_HERE']


def main(client, target_placement_ids):
  # Initialize appropriate service.
  forecast_service = client.GetService('ForecastService', version='v201403')

  # Create prospective line item.
  line_item = {
      'targeting': {
          'inventoryTargeting': {
              'targetedPlacementIds': target_placement_ids
          }
      },
      'creativePlaceholders': [
          {
              'size': {
                  'width': '300',
                  'height': '250'
              }
          },
          {
              'size': {
                  'width': '120',
                  'height': '600'
              }
          }
      ],
      'lineItemType': 'SPONSORSHIP',
      'startDateTimeType': 'IMMEDIATELY',
      'endDateTime': {
          'date': {
              'year': str(date.today().year + 1),
              'month': '9',
              'day': '30'
          },
          'hour': '0',
          'minute': '0',
          'second': '0'
      },
      'costType': 'CPM',
      'costPerUnit': {
          'currencyCode': 'USD',
          'microAmount': '2000000'
      },
      'creativeRotationType': 'EVEN',
      'discountType': 'PERCENTAGE',
      'unitsBought': '50',
      'unitType': 'IMPRESSIONS'
  }

  # Get forecast.
  forecast = forecast_service.GetForecast(line_item)[0]
  matched = long(forecast['matchedUnits'])
  available_percent = (((long(forecast['availableUnits'])/
                         (matched * 1.0)) * 100)
                       if matched != 0 else 0)
  contending_line_items = ([] if 'contendingLineItems' not in forecast
                           else forecast['contendingLineItems'])

  # Display results.
  print '%s %s matched.' % (matched, forecast['unitType'].lower())
  print '%s%% %s available.' % (available_percent, forecast['unitType'].lower())
  print '%d contending line items.' % len(contending_line_items)

  if 'possibleUnits' in forecast:
    possible_percent = (long(forecast['possibleUnits'])/(matched * 1.0)) * 100
    print '%s%% %s possible' % (possible_percent, forecast['unitType'].lower())

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, TARGET_PLACEMENT_IDS)
