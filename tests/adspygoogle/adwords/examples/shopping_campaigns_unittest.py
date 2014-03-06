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

"""Unit tests to cover Shopping Campaign examples."""

__author__ = 'api.msaniscalchi@gmail.com (Mark Saniscalchi)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from examples.adspygoogle.adwords.v201402.shopping_campaigns import add_product_partition_tree
from examples.adspygoogle.adwords.v201402.shopping_campaigns import add_product_scope
from examples.adspygoogle.adwords.v201402.shopping_campaigns import add_shopping_campaign
from examples.adspygoogle.adwords.v201402.shopping_campaigns import get_product_category_taxonomy
from examples.adspygoogle.adwords.v201402.shopping_campaigns import set_product_sales_channel
from tests.adspygoogle.adwords import client
from tests.adspygoogle.adwords import SERVER_V201402
from tests.adspygoogle.adwords import TEST_VERSION_V201402
from tests.adspygoogle.adwords import util
from tests.adspygoogle.adwords import VERSION_V201402



class ShoppingCampaigns(unittest.TestCase):
  """Unittest suite for Shopping Campaign code examples."""

  SERVER = SERVER_V201402
  VERSION = VERSION_V201402
  client.debug = False
  loaded = False

  def setUp(self):
    """Prepare unittest."""
    client.use_mcc = False
    if not self.__class__.loaded:
      self.__class__.merchant_id = '100284316'
      self.__class__.budget_id = util.CreateTestBudget(client)
      self.__class__.campaign_id = util.CreateTestShoppingCampaign(client,
          self.__class__.budget_id, self.__class__.merchant_id)
      self.__class__.ad_group_id = util.CreateTestShoppingAdGroup(client,
          self.__class__.campaign_id)
      self.__class__.loaded = True

  def testAddProductPartitionTree(self):
    """Tests whether we can add a ProductPartitionTree."""
    add_product_partition_tree.main(client, self.__class__.ad_group_id)

  def testAddShoppingCampaign(self):
    """Tests whether we can add a ShoppingCampaign."""
    add_shopping_campaign.main(client, self.__class__.budget_id,
                               self.__class__.merchant_id)

  def testAddProductScope(self):
    """Tests whether we can add a ProductScope."""
    add_product_scope.main(client, self.__class__.campaign_id)

  def testGetProductCategoryTaxonomy(self):
    """Tests whether we can get product bidding category data."""
    get_product_category_taxonomy.main(client)

  def testSetProductSalesChannel(self):
    """Tests whether we can set a ProductSalesChannel Criterion."""
    set_product_sales_channel.main(client, self.__class__.campaign_id)


if __name__ == '__main__':
  if TEST_VERSION_V201402:
    unittest.main()
