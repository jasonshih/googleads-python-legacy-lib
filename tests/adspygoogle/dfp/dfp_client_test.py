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

"""Unit tests to cover DfpClient."""

__author__ = 'Nicholas Chen'

import os
import StringIO
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock

from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfp.DfpClient import DfpClient
from adspygoogle.common.Errors import ValidationError


class DfpClientValidationTest(unittest.TestCase):

  """Tests the validation logic when instantiating DfpClient."""

  def testInitDfpClientWithClientLoginNotSupported(self):
    """Ensures the DFP library throws an error for clientLogin on > v201311."""

    headers = {
        'authToken': 'THIS IS A NO NO AFTER v201311!',
        'applicationName': 'APPLICATION NAME MUST NOT BE EMPTY'
    }
    client = DfpClient(headers=headers)
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      network_service_fine = client.GetNetworkService(version='v201311')
      self.assertRaises(ApiVersionNotSupportedError, client.GetNetworkService,
                        version='v201403')


if __name__ == '__main__':
  unittest.main()
