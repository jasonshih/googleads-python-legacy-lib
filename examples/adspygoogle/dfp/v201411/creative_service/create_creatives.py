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

"""This code example creates new image creatives for a given advertiser.

To determine which companies are advertisers, run get_advertisers.py.
To determine which creatives already exist, run get_all_creatives.py.

Tags: CreativeService.createCreatives
"""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import base64
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils

# Set id of the advertiser (company) that all creatives will be assigned to.
ADVERTISER_ID = 'INSERT_ADVERTISER_COMPANY_ID_HERE'


def main(client, advertiser_id):
  # Initialize appropriate service.
  creative_service = client.GetService('CreativeService', version='v201411')

  # Create creative objects.
  creatives = []
  with open(os.path.join(os.path.split(__file__)[0], '..', '..', 'data',
                         'medium_rectangle.jpg'), 'r') as image:
    image_data = base64.encodestring(image.read())

  for i in xrange(5):
    # Create creative size.
    size = {
        'width': '300',
        'height': '250'
    }

    # Create image asset.
    creative_asset = {
        'type': 'CreativeAsset',
        'fileName': 'image.jpg',
        'assetByteArray': image_data,
        'size': size
    }

    # Create an image creative.
    creative = {
        'type': 'ImageCreative',
        'name': 'Image Creative #%s' % Utils.GetUniqueName(),
        'advertiserId': advertiser_id,
        'destinationUrl': 'http://google.com',
        'size': size,
        'primaryImageAsset': creative_asset
    }

    creatives.append(creative)

  # Add creatives.
  creatives = creative_service.CreateCreatives(creatives)

  # Display results.
  for creative in creatives:
    print ('Image creative with id \'%s\', name \'%s\', and type \'%s\' was '
           'created and can be previewed at %s.'
           % (creative['id'], creative['name'], creative['Creative_Type'],
              creative['previewUrl']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, ADVERTISER_ID)
