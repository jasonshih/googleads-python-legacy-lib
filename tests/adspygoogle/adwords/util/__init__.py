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

"""Helper functions to create objects to run tests with."""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

from adspygoogle.common import Utils
from tests.adspygoogle.adwords import HTTP_PROXY
from tests.adspygoogle.adwords import SERVER_V201402 as SERVER
from tests.adspygoogle.adwords import VERSION_V201402 as VERSION


def CreateTestBudget(client):
  """Creates a budget to run tests with.

  Args:
    client: AdWordsClient client to obtain services from.

  Returns:
    int Budget ID
  """
  budget_service = client.GetBudgetService(SERVER, VERSION, HTTP_PROXY)
  budget = {
      'name': 'Budget #%s' % Utils.GetUniqueName(),
      'amount': {
          'microAmount': '50000000'
      },
      'deliveryMethod': 'STANDARD',
      'period': 'DAILY'
  }
  budget_operations = [{
      'operator': 'ADD',
      'operand': budget
  }]
  return budget_service.Mutate(budget_operations)[0]['value'][0]['budgetId']


def CreateTestCampaign(client):
  """Creates a CPC campaign to run tests with.

  Args:
    client: AdWordsClient client to obtain services from.

  Returns:
    int CampaignId
  """
  campaign_service = client.GetCampaignService(SERVER, VERSION, HTTP_PROXY)
  operations = [{
      'operator': 'ADD',
      'operand': {
          'name': 'Campaign #%s' % Utils.GetUniqueName(),
          'status': 'PAUSED',
          'displaySelect': 'false',
          'biddingStrategyConfiguration': {
              'biddingStrategyType': 'MANUAL_CPC',
              'biddingScheme': {
                  'xsi_type': 'ManualCpcBiddingScheme',
                  'enhancedCpcEnabled': 'false'
              }
          },
          'advertisingChannelType': 'DISPLAY',
          'budget': {
              'budgetId': CreateTestBudget(client)
          }
      }
  }]
  return campaign_service.Mutate(
      operations)[0]['value'][0]['id']


def CreateTestShoppingCampaign(client, budget_id, merchant_id):
  """Creates a shopping campaign to run tests with.

  Note that you need to have linked a Merchant Account.

  Args:
    client: AdWordsClient client to obtain services from.
    budget_id: int id of the budget to be associated with the campaign
    merchant_id: int merchant id to be associated with campaign

  Returns:
    int CampaignId
  """
  # Create campaign
  campaign = {
      'name': 'Shopping campaign #%s' % Utils.GetUniqueName(),
      # The advertisingChannelType is what makes this a shopping campaign
      'advertisingChannelType': 'SHOPPING',
      # Set shared budget (required)
      'budget': {
          'budgetId': budget_id
      },
      'biddingStrategyConfiguration': {
          'biddingStrategyType': 'MANUAL_CPC'
      },
      'settings': [
          # All shopping campaigns need a ShoppingSetting
          {
              'xsi_type': 'ShoppingSetting',
              'salesCountry': 'US',
              'campaignPriority': '0',
              'merchantId': merchant_id
          }
      ]
  }

  operations = [{
      'operator': 'ADD',
      'operand': campaign
  }]

  campaign_service = client.GetCampaignService(SERVER, VERSION, HTTP_PROXY)

  return campaign_service.Mutate(
      operations)[0]['value'][0]['id']


def CreateTestRTBCampaign(client):
  """Creates a CPM campaign to run tests with.

  Args:
    client: AdWordsClient client to obtain services from.

  Returns:
    int CampaignId
  """
  campaign_service = client.GetCampaignService(SERVER, VERSION, HTTP_PROXY)
  operations = [{
      'operator': 'ADD',
      'operand': {
          'name': 'Campaign #%s' % Utils.GetUniqueName(),
          'status': 'PAUSED',
          'biddingStrategyConfiguration': {
              'biddingStrategyType': 'MANUAL_CPM',
              'biddingScheme': {
                  'xsi_type': 'ManualCpmBiddingScheme',
              }
          },
          'advertisingChannelType': 'DISPLAY',
          'budget': {
              'budgetId': CreateTestBudget(client)
          },
          'settings': [{
              'xsi_type': 'RealTimeBiddingSetting',
              'optIn': 'true'
          }]
      }
  }]
  return campaign_service.Mutate(
      operations)[0]['value'][0]['id']


def CreateTestAdGroup(client, campaign_id):
  """Creates a CPC AdGroup to run tests with.

  Args:
    client: AdWordsClient client to obtain services from.
    campaign_id: int ID of a CPC Campaign.

  Returns:
    int AdGroupId
  """
  ad_group_service = client.GetAdGroupService(SERVER, VERSION, HTTP_PROXY)
  operations = [{
      'operator': 'ADD',
      'operand': {
          'campaignId': campaign_id,
          'name': 'AdGroup #%s' % Utils.GetUniqueName(),
          'status': 'ENABLED',
          'biddingStrategyConfiguration': {
              'bids': [
                  {
                      'xsi_type': 'CpcBid',
                      'bid': {
                          'microAmount': '1000000'
                      }
                  }
              ]
          }
      }
  }]
  ad_groups = ad_group_service.Mutate(operations)[0]['value']
  return ad_groups[0]['id']


def CreateTestShoppingAdGroup(client, campaign_id):
  """Create a shopping AdGroup to run tests with

  Args:
    client: AdWordsClient client to obtain services from.
    campaign_id: int ID of a Shopping Campaign.

  Returns:
    int AdGroupId
  """
  adgroup = {
      'campaignId': campaign_id,
      'name': 'AdGroup #%s' % Utils.GetUniqueName()
  }

  operations = [{
      'operator': 'ADD',
      'operand': adgroup
  }]

  adgroup_service = client.GetAdGroupService(SERVER, VERSION, HTTP_PROXY)

  return adgroup_service.Mutate(operations)[0]['value'][0]['id']


def CreateTestCPMAdGroup(client, campaign_id):
  """Creates a CPM AdGroup to run tests with.

  Args:
    client: AdWordsClient client to obtain services from.
    campaign_id: int ID of a CPM Campaign.

  Returns:
    int AdGroupId
  """
  ad_group_service = client.GetAdGroupService(SERVER, VERSION, HTTP_PROXY)
  operations = [{
      'operator': 'ADD',
      'operand': {
          'campaignId': campaign_id,
          'name': 'AdGroup #%s' % Utils.GetUniqueName(),
          'status': 'ENABLED',
          'biddingStrategyConfiguration': {
              'bids': [
                  {
                      'xsi_type': 'CpmBid',
                      'bid': {
                          'microAmount': '1000000'
                      },
                  }
              ]
          }
      }
  }]
  ad_groups = ad_group_service.Mutate(operations)[0]['value']
  return ad_groups[0]['id']


def CreateTestAd(client, ad_group_id):
  """Creates an Ad for running tests with.

  Args:
    client: AdWordsClient client to obtain services from.
    ad_group_id: int ID of the AdGroup the Ad should belong to.

  Returns:
    int AdGroupAdId
  """
  ad_group_ad_service = client.GetAdGroupAdService(SERVER, VERSION, HTTP_PROXY)
  operations = [{
      'operator': 'ADD',
      'operand': {
          'type': 'AdGroupAd',
          'adGroupId': ad_group_id,
          'ad': {
              'type': 'TextAd',
              'url': 'http://www.example.com',
              'displayUrl': 'example.com',
              'description1': 'Visit the Red Planet in style.',
              'description2': 'Low-gravity fun for everyone!',
              'headline': 'Luxury Cruise to Mars'
          },
          'status': 'ENABLED',
      }
  }]
  ads = ad_group_ad_service.Mutate(operations)
  return ads[0]['value'][0]['ad']['id']


def CreateTestKeyword(client, ad_group_id):
  """Creates a Keyword for running tests with.

  Args:
    client: AdWordsClient client to obtain services from.
    ad_group_id: int ID of the AdGroup the Ad should belong to.

  Returns:
    int: KeywordId
  """
  ad_group_criterion_service = client.GetAdGroupCriterionService(
      SERVER, VERSION, HTTP_PROXY)
  operations = [{
      'operator': 'ADD',
      'operand': {
          'type': 'BiddableAdGroupCriterion',
          'adGroupId': ad_group_id,
          'criterion': {
              'xsi_type': 'Keyword',
              'matchType': 'BROAD',
              'text': 'mars cruise'
          }
      }
  }]
  criteria = ad_group_criterion_service.Mutate(operations)
  return criteria[0]['value'][0]['criterion']['id']


def CreateTestLabel(client):
  """Creates a Label for running tests with.

  Args:
    client: AdWordsClient client to obtain services from.

  Returns:
    int: LabelId
  """
  label_service = client.GetLabelService()

  operations = [
      {
          'operator': 'ADD',
          'operand': {
              'xsi_type': 'TextLabel',
              'name': 'Test Label - %s' % Utils.GetUniqueName(),
          }
      }
  ]

  labels = label_service.Mutate(operations)[0]
  label = labels['value'][0]
  return label['id']


def CreateTestPlacement(client, ad_group_id):
  """Creates a Placement for running tests with.

  Args:
    client: AdWordsClient client to obtain services from.
    ad_group_id: int ID of the AdGroup the Ad should belong to.

  Returns:
    int: KeywordId
  """
  ad_group_criterion_service = client.GetAdGroupCriterionService(
      SERVER, VERSION, HTTP_PROXY)
  operations = [{
      'operator': 'ADD',
      'operand': {
          'xsi_type': 'BiddableAdGroupCriterion',
          'adGroupId': ad_group_id,
          'criterion': {
              'xsi_type': 'Placement',
              'url': 'http://mars.google.com'
          },
      }
  }]
  criteria = ad_group_criterion_service.Mutate(operations)
  return criteria[0]['value'][0]['criterion']['id']


def CreateTestLocationExtension(client, campaign_id):
  """Creates a Location Extension for testing.

  Args:
    client: AdWordsClient client to obtain services from.
    campaign_id: int ID of a CPC Campaign.

  Returns:
    int Location Extension ID
  """
  geo_location_service = client.GetGeoLocationService(
      SERVER, VERSION, HTTP_PROXY)
  campaign_ad_extension_service = client.GetCampaignAdExtensionService(
      SERVER, VERSION, HTTP_PROXY)
  selector = {
      'addresses': [
          {
              'streetAddress': '1600 Amphitheatre Parkway',
              'cityName': 'Mountain View',
              'provinceCode': 'US-CA',
              'provinceName': 'California',
              'postalCode': '94043',
              'countryCode': 'US'
          }
      ]
  }
  geo_locations = geo_location_service.Get(selector)
  # Construct operations and add campaign ad extension.
  operations = [
      {
          'operator': 'ADD',
          'operand': {
              'xsi_type': 'CampaignAdExtension',
              'campaignId': campaign_id,
              'adExtension': {
                  'xsi_type': 'LocationExtension',
                  'address': geo_locations[0]['address'],
                  'geoPoint': geo_locations[0]['geoPoint'],
                  'encodedLocation': geo_locations[0]['encodedLocation'],
                  'source': 'ADWORDS_FRONTEND'
              }
          }
      }
  ]
  ad_extensions = campaign_ad_extension_service.Mutate(operations)[0]
  ad_extension = ad_extensions['value'][0]
  return ad_extension['adExtension']['id']


def GetExperimentIdForCampaign(client, campaign_id):
  """Retreives the ID of an ACTIVE experiment for the specified campaign.

  Args:
    client: AdWordsClient client to obtain services from.
    campaign_id: int ID of a CPC Campaign.

  Returns:
    int Experiment ID
  """
  selector = {
      'fields': ['Id'],
      'predicates': [{
          'field': 'CampaignId',
          'operator': 'EQUALS',
          'values': [campaign_id]
      }, {
          'field': 'Status',
          'operator': 'EQUALS',
          'values': ['ACTIVE']
      }]
  }
  experiment_service = client.GetExperimentService(SERVER, VERSION, HTTP_PROXY)
  page = experiment_service.get(selector)[0]
  return page['entries'][0]['id']


def RemoveAllFeeds(client):
  """Removes all Feeds associated with the account.

  Args:
    client: AdWordsClient client to obtain services from.
  """
  feed_service = client.GetFeedService()

  selector = {
      'fields': ['Id'],
      'predicates': [{
          'field': 'FeedStatus',
          'operator': 'EQUALS',
          'values': ['ENABLED']
      }, {
          'field': 'Origin',
          'operator': 'EQUALS',
          'values': ['USER']
      }]
  }

  response = feed_service.get(selector)[0]

  if 'entries' in response:
    # Use feeds in response to build operations for delete operation.
    operations = [{
        'operator': 'REMOVE',
        'operand': {
            'xsi_type': 'Feed',
            'id': feed['id']
        }
    } for feed in response['entries']]
  # Delete the feeds
  feed_service.Mutate(operations)
