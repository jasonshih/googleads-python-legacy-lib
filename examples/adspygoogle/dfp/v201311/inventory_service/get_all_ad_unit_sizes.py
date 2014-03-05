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

"""This code example gets all ad unit sizes defined in a network.

To create ad units, run create_ad_units.py

Tags: InventoryService.getAdUnitSizesByStatement
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
  inventory_service = client.GetService('InventoryService', version='v201311')
  statement = DfpUtils.FilterStatement()

  # Get ad units by statement.
  while True:
    response = inventory_service.GetAdUnitSizesByStatement(
        statement.ToStatement())[0]
    ad_unit_sizes = response.get('results')
    if ad_unit_sizes:
      # Display results.
      for ad_unit_size in ad_unit_sizes:
        print ('Ad unit size of dimensions %s was found.' %
               (ad_unit_size['fullDisplayString']))
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
