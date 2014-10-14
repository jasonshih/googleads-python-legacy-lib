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

"""This example adds a label to multiple campaigns.

The AdWordsClient is pulling credentials and properties from a
"adwords_api_auth.pkl" file. By default, it looks for this file in your home
directory.

Tags: CampaignService.mutateLabel
"""

__author__ = 'Mark Saniscalchi'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

from adspygoogle import AdWordsClient


CAMPAIGN_ID1 = 'INSERT_FIRST_CAMPAIGN_ID_HERE'
CAMPAIGN_ID2 = 'INSERT_SECOND_CAMPAIGN_ID_HERE'
LABEL_ID = 'INSERT_LABEL_ID_HERE'


def main(client, campaign_id1, campaign_id2, label_id):
  # Initialize appropriate service.
  campaign_service = client.GetCampaignService(version='v201409')

  operations = [
      {
          'operator': 'ADD',
          'operand': {
              'campaignId': campaign_id1,
              'labelId': label_id,
          }
      },
      {
          'operator': 'ADD',
          'operand': {
              'campaignId': campaign_id2,
              'labelId': label_id,
          }
      }
  ]

  result = campaign_service.MutateLabel(operations)[0]

  # Display results.
  for label in result['value']:
    print ('CampaignLabel with campaignId \'%s\' and labelId \'%s\' was added.'
           % (label['campaignId'], label['labelId']))


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, CAMPAIGN_ID1, CAMPAIGN_ID2, LABEL_ID)
