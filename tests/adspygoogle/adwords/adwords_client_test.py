#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Unit tests to cover AdWordsClient."""

__author__ = ('api.kwinter@gmail.com (Kevin Winter)',
              'api.jdilallo@gmail.com (Joseph DiLallo)')

import os
import StringIO
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock

from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.common.Errors import ValidationError


DEFAULT_HEADERS = {
    'userAgent': 'Foo Bar',
    'developerToken': 'devtoken'
}


class AdWordsClientValidationTest(unittest.TestCase):
  """Tests the validation logic when instantiating AdWordsClient."""

  def testOAuth2CredentialsOnly(self):
    """Tests that specifying solely oauth_credentials works."""
    headers = DEFAULT_HEADERS.copy()
    headers['oauth2credentials'] = 'credential!'
    client = AdWordsClient(headers=headers)
    self.assertTrue(client.oauth2credentials)

  def testOAuthCredentialsOthersBlank(self):
    """Tests that oauth_credentials with other auth blank works."""
    headers = DEFAULT_HEADERS.copy()
    headers['oauth2credentials'] = 'credential!'
    headers['email'] = ''
    headers['password'] = ''
    headers['authToken'] = ''
    client = AdWordsClient(headers=headers)
    self.assertTrue(client.oauth2credentials)

  def testNonStrictThrowsValidationError(self):
    """Tests that even when using non-strict mode, we still raise a
    ValidationError when no auth credentials are provided."""
    headers = DEFAULT_HEADERS.copy()
    config = {'strict': 'n'}

    def Run():
      _ = AdWordsClient(headers=headers, config=config)
    self.assertRaises(ValidationError, Run)


class AdWordsClientServiceTest(unittest.TestCase):
  """Tests for retrieving SOAP services via AdWordsClient."""

  def setUp(self):
    """Prepare unittest."""
    self.client = AdWordsClient(headers={'oauth2credentials': 'credential!',
                                         'userAgent': 'USER AGENT',
                                         'developerToken': 'DEV TOKEN'})

  def testGetAlertService(self):
    """AlertService shouldn't be created as of v201409"""
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      with self.assertRaises(ValidationError):
        service = self.client.GetAlertService()

  def testGetAlertService_v201406(self):
    """AlertService should be created in v201406 or earlier."""
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetAlertService(version='v201406')
      self.assertEquals('AlertService', service._service_name)

  def testGetBudgetService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetBudgetService()
      self.assertEquals('BudgetService', service._service_name)

  def testGetAdGroupFeedService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetAdGroupFeedService()
      self.assertEquals('AdGroupFeedService', service._service_name)

  def testGetCampaignFeedService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetCampaignFeedService()
      self.assertEquals('CampaignFeedService', service._service_name)

  def testGetCustomerFeedService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetCustomerFeedService()
      self.assertEquals('CustomerFeedService', service._service_name)

  def testGetFeedItemService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetFeedItemService()
      self.assertEquals('FeedItemService', service._service_name)

  def testGetFeedMappingService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetFeedMappingService()
      self.assertEquals('FeedMappingService', service._service_name)

  def testGetFeedService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetFeedService()
      self.assertEquals('FeedService', service._service_name)

  def testGetCampaignSharedSetService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetCampaignSharedSetService()
      self.assertEquals('CampaignSharedSetService', service._service_name)

  def testGetSharedSetService(self):
    """SharedSetService now available in v201406."""
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetSharedSetService()
      self.assertEquals('SharedSetService', service._service_name)

  def testGetSharedCriterionService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetSharedCriterionService()
      self.assertEquals('SharedCriterionService', service._service_name)

  def testGetAdGroupBidModifierService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetAdGroupBidModifierService()
      self.assertEquals('AdGroupBidModifierService', service._service_name)

  def testGetOfflineConversionFeedService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetOfflineConversionFeedService()
      self.assertEquals('OfflineConversionFeedService', service._service_name)

  def testGetLabelService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetLabelService()
      self.assertEquals('LabelService', service._service_name)


if __name__ == '__main__':
  unittest.main()
