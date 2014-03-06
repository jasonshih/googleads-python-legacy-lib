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

"""This example updates a campaign by setting its status to PAUSED.

To get campaigns, run get_campaigns.py.

Tags: CampaignService.mutate
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient


campaign_id = 'INSERT_CAMPAIGN_ID_HERE'


def main(client, campaign_id):
  # Initialize appropriate service.
  campaign_service = client.GetCampaignService(version='v201402')

  # Construct operations and update campaign.
  operations = [{
      'operator': 'SET',
      'operand': {
          'id': campaign_id,
          'status': 'PAUSED'
      }
  }]
  campaigns = campaign_service.Mutate(operations)[0]

  # Display results.
  for campaign in campaigns['value']:
    print ('Campaign with name \'%s\' and id \'%s\' was updated.'
           % (campaign['name'], campaign['id']))

  print
  print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                             client.GetOperations()))


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, campaign_id)
