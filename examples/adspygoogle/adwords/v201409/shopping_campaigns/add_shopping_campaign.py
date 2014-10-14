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

"""This example adds a Shopping campaign.

Tags: CampaignService.mutate, AdGroupService.mutate, AdGroupAdService.mutate
"""

__author__ = 'api.msaniscalchi@gmail.com (Mark Saniscalchi)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient
from adspygoogle.common import Utils


BUDGET_ID = 'INSERT_BUDGET_ID_HERE'


MERCHANT_ID = 'INSERT_MERCHANT_ID_HERE'


def main(client, budget_id, merchant_id):
  # Create campaign
  campaign = {
      'name': 'Shopping campaign #%s' % Utils.GetUniqueName(),
      # The advertisingChannelType is what makes this a shopping campaign
      'advertisingChannelType': 'SHOPPING',
      # Set shared budget (required)
      'budget': {
          'budgetId': budget_id
      },
      'biddingStrategyConfiguration': {
          'biddingStrategyType': 'MANUAL_CPC'
      },
      'settings': [
          # All shopping campaigns need a ShoppingSetting
          {
              'xsi_type': 'ShoppingSetting',
              'salesCountry': 'US',
              'campaignPriority': '0',
              'merchantId': merchant_id
          }
      ]
  }

  campaign_operations = [{
      'operator': 'ADD',
      'operand': campaign
  }]

  # Make the mutate request to add the Shopping Campaign
  c_result = client.GetCampaignService(version='v201409').Mutate(
      campaign_operations)[0]

  for campaign in c_result['value']:
    print 'Campaign with name \'%s\' and ID \'%s\' was added.' % (
        campaign['name'], campaign['id'])

  # Create AdGroup
  adgroup = {
      'campaignId': campaign['id'],
      'name': 'AdGroup #%s' % Utils.GetUniqueName()
  }

  adgroup_operations = [{
      'operator': 'ADD',
      'operand': adgroup
  }]

  # Make the mutate request to add the AdGroup to the Shopping Campaign
  a_result = client.GetAdGroupService(version='v201409').Mutate(
      adgroup_operations)[0]

  for adgroup in a_result['value']:
    print 'AdGroup with name \'%s\' and ID \'%s\' was added.' % (
        adgroup['name'], adgroup['id'])

  # Create AdGroup Ad
  adgroup_ad = {
      'adGroupId': adgroup['id'],
      # Create ProductAd
      'ad': {
          'xsi_type': 'ProductAd'
      }
  }

  ad_operations = [{
      'operator': 'ADD',
      'operand': adgroup_ad
  }]

  # Make the mutate request to add the ProductAd to the AdGroup
  ad_result = client.GetAdGroupAdService(version='v201409').Mutate(
      ad_operations)[0]

  for adgroup_ad in ad_result['value']:
    print 'ProductAd with ID \'%s\' was added.' % adgroup_ad['ad']['id']

if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, BUDGET_ID, MERCHANT_ID)
