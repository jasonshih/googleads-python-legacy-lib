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

"""This code example creates a new template creative for a given advertiser.

To determine which companies are advertisers, run get_advertisers.py.
To determine which creative templates exist, run
get_all_creative_templates.py.

Tags: CreativeService.createCreative
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

# Set id of the advertiser (company) that the creative will be assigned to.
ADVERTISER_ID = 'INSERT_ADVERTISER_COMPANY_ID_HERE'


def main(client, advertiser_id):
  # Initialize appropriate service.
  creative_service = client.GetService('CreativeService', version='v201408')

  # Use the image banner with optional third party tracking template.
  creative_template_id = '10000680'

  image_data = open(os.path.join(__file__[:__file__.rfind('/')], '..', 'data',
                                 'medium_rectangle.jpg'), 'r').read()
  image_data = base64.encodestring(image_data)
  # Create creative from templates.
  creative = {
      'type': 'TemplateCreative',
      'name': 'Template Creative #%s' % Utils.GetUniqueName(),
      'advertiserId': advertiser_id,
      'size': {'width': '300', 'height': '250'},
      'creativeTemplateId': creative_template_id,
      'creativeTemplateVariableValues': [
          {
              'type': 'AssetCreativeTemplateVariableValue',
              'uniqueName': 'Imagefile',
              'assetByteArray': image_data,
              'fileName': 'image%s.jpg' % Utils.GetUniqueName()
          },
          {
              'type': 'LongCreativeTemplateVariableValue',
              'uniqueName': 'Imagewidth',
              'value': '300'
          },
          {
              'type': 'LongCreativeTemplateVariableValue',
              'uniqueName': 'Imageheight',
              'value': '250'
          },
          {
              'type': 'UrlCreativeTemplateVariableValue',
              'uniqueName': 'ClickthroughURL',
              'value': 'www.google.com'
          },
          {
              'type': 'StringCreativeTemplateVariableValue',
              'uniqueName': 'Targetwindow',
              'value': '_blank'
          }
      ]
  }

  # Call service to create the creative.
  creative = creative_service.CreateCreative(creative)[0]

  # Display results.
  print ('Template creative with id \'%s\', name \'%s\', and type \'%s\' was '
         'created and can be previewed at %s.'
         % (creative['id'], creative['name'], creative['Creative_Type'],
            creative['previewUrl']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, ADVERTISER_ID)
