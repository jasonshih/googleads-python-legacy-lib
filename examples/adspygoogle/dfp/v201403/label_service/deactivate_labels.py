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

"""This code example deactivates all active Labels.

To determine which labels exist, run get_all_labels.py. This feature is only
available to DFP premium solution networks."""

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
  label_service = client.GetService('LabelService', version='v201403')

  # Create query.
  values = [{
      'key': 'isActive',
      'value': {
          'xsi_type': 'TextValue',
          'value': 'true'
      }
  }]
  query = 'WHERE isActive = :isActive'
  statement = DfpUtils.FilterStatement(query, values)

  labels_deactivated = 0

  # Get labels by statement.
  while True:
    response = label_service.GetLabelsByStatement(statement.ToStatement())[0]
    labels = response.get('results')
    if labels:
      for label in labels:
        print ('Label with id \'%s\' and name \'%s\' will be '
               'deactivated.' % (label['id'], label['name']))
      # Perform action.
      result = label_service.PerformLabelAction({'type': 'DeactivateLabels'},
                                                statement.ToStatement())[0]
      if result and int(result['numChanges']) > 0:
        labels_deactivated += int(result['numChanges'])
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  # Display results.
  if labels_deactivated > 0:
    print 'Number of labels deactivated: %s' % labels_deactivated
  else:
    print 'No labels were deactivated.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
