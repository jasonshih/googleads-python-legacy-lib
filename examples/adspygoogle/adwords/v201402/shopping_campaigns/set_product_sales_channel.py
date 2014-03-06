#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
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

"""This example sets the product sales channel.

Tags: CampaignCriterionService.mutate
"""

__author__ = 'api.msaniscalchi@gmail.com (Mark Saniscalchi)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient


CAMPAIGN_ID = 'INSERT_CAMPAIGN_ID_HERE'


def main(client, campaign_id):
  # ProductSalesChannel is a fixedId criterion, with the possible values
  # defined here.
  ONLINE = '200'
  LOCAL = '201'

  product_sales_channel = {
      'xsi_type': 'ProductSalesChannel',
      'id': ONLINE
  }

  campaign_criterion = {
      'campaignId': campaign_id,
      'criterion': product_sales_channel
  }

  operations = [{
      'operator': 'ADD',
      'operand': campaign_criterion
  }]

  result = client.GetCampaignCriterionService(version='v201402').Mutate(
      operations)[0]

  for criterion in result['value']:
    print 'Added ProductSalesChannel CampaignCriterion with ID: %s' % (
        criterion['criterion']['id'])

if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, CAMPAIGN_ID)
