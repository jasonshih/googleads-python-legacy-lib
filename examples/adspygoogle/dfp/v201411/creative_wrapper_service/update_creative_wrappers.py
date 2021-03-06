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

"""This code example updates a creative wrapper to the 'OUTER' wrapping order.

To determine which creative wrappers exist, run get_all_creative_wrappers.py.

Tags: CreativeWrapperService.getCreativeWrappersByStatement
Tags: CreativeWrapperService.updateCreativeWrappers
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

# Set the ID of the creative wrapper to update.
CREATIVE_WRAPPER_ID = 'INSERT_CREATIVE_WRAPPER_ID_HERE'


def main(client, creative_wrapper_id):
  # Initialize appropriate service.
  creative_wrapper_service = client.GetService('CreativeWrapperService',
                                               version='v201411')

  # Create statement to get a creative wrapper by ID.
  values = [{
      'key': 'creativeWrapperId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': creative_wrapper_id
      }
  }]
  query = 'WHERE id = :creativeWrapperId'
  statement = DfpUtils.FilterStatement(query, values)

  # Get creative wrappers.
  response = creative_wrapper_service.GetCreativeWrappersByStatement(
      statement.ToStatement())[0]
  creative_wrappers = response.get('results')

  if creative_wrappers:
    for creative_wrapper in creative_wrappers:
      creative_wrapper['ordering'] = 'OUTER'

    # Update the creative wrappers on the server.
    creative_wrappers = creative_wrapper_service.UpdateCreativeWrappers(
        creative_wrappers)

    # Display results.
    for creative_wrapper in creative_wrappers:
      print (('Creative wrapper with ID \'%s\' and wrapping order \'%s\' '
              'was updated.') % (creative_wrapper['id'],
                                 creative_wrapper['ordering']))
  else:
    print 'No creative wrappers found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, CREATIVE_WRAPPER_ID)
