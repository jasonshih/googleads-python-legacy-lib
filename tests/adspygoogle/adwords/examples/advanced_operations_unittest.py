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

"""Unit tests to cover Advanced Operations examples."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from examples.adspygoogle.adwords.v201409.advanced_operations import add_ad_customizer
from examples.adspygoogle.adwords.v201409.advanced_operations import add_ad_group_bid_modifier
from examples.adspygoogle.adwords.v201409.advanced_operations import add_click_to_download_ad
from examples.adspygoogle.adwords.v201409.advanced_operations import add_site_links
from examples.adspygoogle.adwords.v201409.advanced_operations import add_text_ad_with_upgraded_urls
from examples.adspygoogle.adwords.v201409.advanced_operations import get_ad_group_bid_modifier
from examples.adspygoogle.adwords.v201409.advanced_operations import use_shared_bidding_strategy
from tests.adspygoogle.adwords import client
from tests.adspygoogle.adwords import util
from tests.adspygoogle.adwords import SERVER_V201409
from tests.adspygoogle.adwords import TEST_VERSION_V201409
from tests.adspygoogle.adwords import VERSION_V201409


class AdvancedOperations(unittest.TestCase):

  """Unittest suite for Advanced Operations code examples."""

  SERVER = SERVER_V201409
  VERSION = VERSION_V201409
  client.debug = False
  loaded = False

  def setUp(self):
    """Prepare unittest."""
    if not self.loaded:
      self.campaign_id = util.CreateTestCampaign(client)
      self.ad_group_id_1 = util.CreateTestAdGroup(client, self.campaign_id)
      self.ad_group_id_2 = util.CreateTestAdGroup(client, self.campaign_id)

  def testAddAdCustomizer(self):
    util.RemoveAllFeeds(client)
    add_ad_customizer.main(client, [self.ad_group_id_1, self.ad_group_id_2])

  def testAddAndRetrieveAdGroupBidModifier(self):
    add_ad_group_bid_modifier.main(client, self.ad_group_id_1, '1.5')
    get_ad_group_bid_modifier.main(client)

  def testAddClickToDownloadAd(self):
    """Tests whether we can create an account."""
    add_click_to_download_ad.main(client, self.ad_group_id_1)

  def testAddSiteLink(self):
    """Test whether we can get account alerts."""
    add_site_links.main(client, self.campaign_id)

  def testAddTextAdWithUpgradedUrls(self):
    """Test whether we can add a text ad using upgraded urls"""
    add_text_ad_with_upgraded_urls.main(client, self.ad_group_id_1)

  def testUseSharedBiddingStrategy(self):
    use_shared_bidding_strategy.main(client, None)


if __name__ == '__main__':
  if TEST_VERSION_V201409:
    unittest.main()
