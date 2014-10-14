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

"""Handler to make calls against the AdWords API."""

__author__ = 'Mark Saniscalchi'

import time

from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.adwords.AdWordsErrors import AdWordsError
from adspygoogle.common import Utils
from demo import VERSION
import httplib2
from oauth2client.client import OAuth2Credentials


class APIHandler(object):
  """Handler for the AdWords API using the Ads Python Client Libraries."""

  # The URL used to refresh the access token.
  _REFRESH_URL = 'https://accounts.google.com/o/oauth2/token'
  # The user-agent sent in requests from this demo.
  _USER_AGENT = 'AppEngine Demo v%s' % VERSION

  def __init__(self, client_id, client_secret, refresh_token, mcc_cid,
               dev_token, debug=False):
    """Initializes an APIHandler.

    Args:
      client_id:
      client_secret:
      refresh_token:
      mcc_cid:
      dev_token:
      debug:
    """
    credentials = OAuth2Credentials(None, client_id, client_secret,
                                    refresh_token, None, self._REFRESH_URL,
                                    self._USER_AGENT)
    credentials.refresh(httplib2.Http())

    headers = {
        'clientCustomerId': mcc_cid,
        'userAgent': self._USER_AGENT,
        'developerToken': dev_token,
        'validateOnly': 'n',
        'partialFailure': 'n',
        'oauth2credentials': credentials
    }
    # App Engine doesn't allow you to write to the disk. Thus, we need to
    # explicitly turn off logging. Though, if debugging is enabled, the
    # data from STDOUT will be redirected to app engine's debugging console.
    # Note that we also specify that we want to use ElementTree here; see the
    # README for more information if you would rather use PyXML.
    config = {
        'debug': Utils.BoolTypeConvert(debug),
        'xml_log': 'n',
        'request_log': 'n',
        'pretty_xml': 'n',
        'xml_parser': '2',  # We're using ElementTree.
        'compress': 'n'
    }

    self.client = AdWordsClient(headers, config)
    self.client.use_mcc = True

  def AddAdGroup(self, client_customer_id, campaign_id, name, status):
    """Create a new ad group.

    Args:
      client_customer_id: str Client Customer Id used to create the AdGroup.
      campaign_id: str Id of the campaign to use.
      name: str Name to assign to the AdGroup.
      status: str Status to assign to the AdGroup when it is created.
    """
    self.client.use_mcc = False
    self.client.SetClientCustomerId(client_customer_id)

    ad_group_service = self.client.GetAdGroupService()
    operations = [{
        'operator': 'ADD',
        'operand': {
            'campaignId': campaign_id,
            'name': name,
            'status': status
        }
    }]
    ad_group_service.Mutate(operations)

  def AddBudget(self, client_customer_id, micro_amount):
    """Create a new Budget with the given microAmount.

    Args:
      client_customer_id: str Client Customer Id used to create Budget.
      micro_amount: str The budget represented in micros.

    Returns:
      str BudgetId of the newly created Budget.
    """
    self.client.use_mcc = False
    self.client.SetClientCustomerId(client_customer_id)

    budget_service = self.client.GetBudgetService()

    operations = [{
        'operator': 'ADD',
        'operand': {
            'name': 'Budget #%s' % time.time(),
            'period': 'DAILY',
            'amount': {
                'microAmount': micro_amount
            },
            'deliveryMethod': 'STANDARD'
        }
    }]

    return budget_service.Mutate(operations)[0]['value'][0]['budgetId']

  def AddCampaign(self, client_customer_id, campaign_name, ad_channel_type,
                  budget):
    """Add a Campaign to the client account.

    Args:
      ad_channel_type: str Primary serving target the campaign's ads.
      budget: str a budget amount (in micros) to use.
      campaign_name: str Name of the campaign to be added.
      client_customer_id: str Client Customer Id to use when creating Campaign.
    """
    self.client.use_mcc = False
    self.client.SetClientCustomerId(client_customer_id)
    campaign_service = self.client.GetCampaignService()
    budget_id = self.AddBudget(client_customer_id, budget)

    operations = [{
        'operator': 'ADD',
        'operand': {
            'name': campaign_name,
            'status': 'PAUSED',
            'biddingStrategyConfiguration': {
                'biddingStrategyType': 'MANUAL_CPC',
                'biddingScheme': {
                    'xsi_type': 'ManualCpcBiddingScheme',
                    'enhancedCpcEnabled': 'false'
                }
            },
            'budget': {
                'budgetId': budget_id
            },
            'advertisingChannelType': ad_channel_type,
            'settings': [
                {
                    'xsi_type': 'KeywordMatchSetting',
                    'optIn': 'false'
                }
            ]
        }
    }]

    campaign_service.Mutate(operations)

  def GetAccounts(self):
    """Return the client accounts associated with the user's MCC account.

    Returns:
      list List of ManagedCustomer data objects.
    """
    selector = {
        'fields': ['CustomerId', 'Login', 'CanManageClients']
    }

    self.client.use_mcc = True
    accounts = self.client.GetManagedCustomerService().Get(selector)[0]
    self.client.use_mcc = False

    return accounts['entries']

  def GetAdGroups(self, client_customer_id, campaign_id):
    """Retrieves all AdGroups for the given campaign that haven't been removed.

    Args:
      client_customer_id: str Client Customer Id being used in API request.
      campaign_id: str id of the campaign for which to fetch ad groups.

    Returns:
      list List of AdGroup data objects.
    """
    self.client.use_mcc = False
    self.client.SetClientCustomerId(client_customer_id)
    selector = {
        'fields': ['Id', 'Name', 'Status'],
        'predicates': [
            {
                'field': 'CampaignId',
                'operator': 'EQUALS',
                'values': [campaign_id]
            },
            {
                'field': 'Status',
                'operator': 'NOT_EQUALS',
                'values': ['REMOVED']
            }
        ]
    }
    adgroups = self.client.GetAdGroupService().Get(selector)[0]

    if int(adgroups['totalNumEntries']) > 0:
      return adgroups['entries']
    else:
      return None

  def GetBudget(self, client_customer_id, budget_id):
    """Return a Budget with the associated budgetId.

    Args:
      client_customer_id: str Client Customer Id to which the budget belongs.
      budget_id: str id of the budget we want to examine.

    Returns:
      Budget A Budget data object.
    """
    self.client.use_mcc = False
    self.client.SetClientCustomerId(client_customer_id)
    selector = {
        'fields': ['BudgetId', 'BudgetName', 'BudgetStatus', 'Amount',
                   'DeliveryMethod', 'BudgetReferenceCount',
                   'IsBudgetExplicitlyShared'],
        'predicates': [
            {
                'field': 'BudgetId',
                'operator': 'EQUALS',
                'values': [budget_id]
            }
        ]
    }
    budgets = self.client.GetBudgetService().Get(selector)[0]

    if int(budgets['totalNumEntries']) > 0:
      return budgets['entries'][0]
    else:
      return None

  def GetCampaigns(self, client_customer_id):
    """Returns a client account's Campaigns that haven't been removed.

    Args:
      client_customer_id: str Client Customer Id used to retrieve Campaigns.

    Returns:
      list List of Campaign data objects.
    """
    self.client.SetClientCustomerId(client_customer_id)
    self.client.use_mcc = False
    # A somewhat hackish workaround for "The read operation timed out" error,
    # which could be triggered on AppEngine's end if the request is too large
    # and is taking too long.
    max_tries = 3
    today = time.strftime('%Y%m%d', time.localtime())
    for i in xrange(1, max_tries + 1):
      try:
        selector = {
            'fields': ['Id', 'Name', 'Status', 'BudgetId', 'Amount'],
            'predicates': [
                {
                    'field': 'Status',
                    'operator': 'NOT_EQUALS',
                    'values': ['REMOVED']
                }
            ],
            'dateRange': {
                'min': today,
                'max': today
            }
        }
        campaigns = self.client.GetCampaignService().Get(selector)[0]
        if int(campaigns['totalNumEntries']) > 0:
          return campaigns['entries']
        else:
          return None
      except Exception, e:
        if i == max_tries:
          raise AdWordsError(e)
        continue

  def UpdateBudget(self, client_customer_id, budget_id, micro_amount,
                   delivery_method):
    """Update a Budget with the given budgetId.

    Args:
      client_customer_id: str Client Customer Id used to update Budget.
      budget_id: str Id of the budget to be updated.
      micro_amount: str New value for the microAmount field.
      delivery_method: str New value for the deliveryMethod field.
    """
    self.client.SetClientCustomerId(client_customer_id)
    self.client.use_mcc = False
    operations = [{
        'operator': 'SET',
        'operand': {
            'budgetId': budget_id,
            'amount': {
                'microAmount': micro_amount
            },
            'deliveryMethod': delivery_method
        }
    }]
    self.client.GetBudgetService().Mutate(operations)
