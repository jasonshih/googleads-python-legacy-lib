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

"""This code example creates new ad units.

To determine which ad units exist, run get_all_ad_units.py

Tags: InventoryService.createAdUnits
"""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils

PARENT_AD_UNIT_ID = 'INSERT_AD_UNIT_ID_HERE'


def main(client, parent_id):
  # Initialize appropriate service.
  inventory_service = client.GetService('InventoryService', version='v201403')

  # Create ad unit size.
  ad_unit_size = {
      'size': {
          'width': '300',
          'height': '250'
      },
      'environmentType': 'BROWSER'
  }

  # Create ad unit objects.
  ad_unit = {
      'name': 'Ad_unit_%s' % Utils.GetUniqueName(),
      'parentId': parent_id,
      'description': 'Ad unit description.',
      'targetWindow': 'BLANK',
      'targetPlatform': 'WEB',
      'adUnitSizes': [ad_unit_size]
  }

  # Add ad units.
  ad_units = inventory_service.CreateAdUnits([ad_unit])

  # Display results.
  for ad_unit in ad_units:
    print ('Ad unit with ID \'%s\' and name \'%s\' was created.'
           % (ad_unit['id'], ad_unit['name']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, PARENT_AD_UNIT_ID)
