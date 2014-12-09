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


"""This example adds a feed that syncs feed items from a Google My Business
(GMB) account and associates the feed with a customer.

Credentials and configurations are pulled from adwords_api_auth.pkl and
adwords_api_config.pkl respectively.

Tags: CustomerFeedService.mutate, FeedItemService.mutate
Tags: FeedMappingService.mutate, FeedService.mutate
"""

__author__ = 'api.msaniscalchi@gmail.com (Mark Saniscalchi)'

import os
import sys
import time
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient
from adspygoogle.common import Utils
from adspygoogle.common.Errors import Error


GMB_EMAIL_ADDRESS = 'INSERT_GMB_EMAIL_ADDRESS_HERE'


# To obtain an access token for your GMB account, you can run the
# generate_refresh_token.py example, selecting the "Other" product and setting
# the scope to "https://www.google.com/local/add".
GMB_ACCESS_TOKEN = 'INSERT_GMB_OAUTH_ACCESS_TOKEN_HERE'


def main(client, gmb_email_address, gmb_access_token):
  # The placeholder type for location extensions.
  # See the Placeholder reference page for a list of all the placeholder types
  # and fields:
  # https://developers.google.com/adwords/api/docs/appendix/placeholders
  placeholder_location = 7

  # The maximum number of CustomerFeed ADD operation attempts to make before
  # throwing an exception.
  max_customer_feed_add_attempts = 10

  # Create a feed that will sync to the Google My Business account specified by
  # gmb_email_address. Do not add FeedAttributes to this object,
  # as AdWords will add them automatically because this will be a
  # system generated feed.
  feed = {
      'name': 'Google My Business feed #%s' % Utils.GetUniqueName(),
      'systemFeedGenerationData': {
          'xsi_type': 'PlacesLocationFeedData',
          'oAuthInfo': {
              'httpMethod': 'GET',
              'httpRequestUrl': 'https://www.google.com/local/add',
              'httpAuthorizationHeader': 'Bearer %s' % gmb_access_token
          },
          'emailAddress': gmb_email_address,
      },
      # Since this feed's feed items will be managed by AdWords, you must set
      # its origin to ADWORDS.
      'origin': 'ADWORDS'
  }

  # Create an operation to add the feed.
  gmb_operations = [{
      'operator': 'ADD',
      'operand': feed
  }]

  gmb_response = client.GetFeedService(version='v201406').Mutate(
      gmb_operations)[0]
  added_feed = gmb_response['value'][0]
  print 'Added GMB feed with ID: %d\n' % added_feed['id']

  # Add a CustomerFeed that associates the feed with this customer for the
  # LOCATION placeholder type.
  customer_feed = {
      'feedId': added_feed['id'],
      'placeholderTypes': [placeholder_location],
      'matchingFunction': {
          'operator': 'IDENTITY',
          'lhsOperand': {
              'xsi_type': 'FunctionArgumentOperand',
              'type': 'BOOLEAN',
              'booleanValue': True
          }
      }
  }

  customer_feed_operation = {
      'xsi_type': 'CustomerFeedOperation',
      'operator': 'ADD',
      'operand': customer_feed
  }

  customer_feed_service = client.GetCustomerFeedService(version='v201406')
  added_customer_feed = None

  i = 0
  while i < max_customer_feed_add_attempts and added_customer_feed is None:
    try:
      added_customer_feed = customer_feed_service.Mutate([
          customer_feed_operation])[0]['value'][0]
    except:
      # Wait using exponential backoff policy
      sleep_seconds = 2 ** i
      print ('Attempt %d to add the CustomerFeed was not successful.'
             'Waiting %d seconds before trying again.\n' % (i, sleep_seconds))
      time.sleep(sleep_seconds)
    i += 1

  if added_customer_feed is None:
    raise Error('Could not create the CustomerFeed after %s attempts. Please'
                ' retry the CustomerFeed ADD operation later.'
                % max_customer_feed_add_attempts)

  print ('Added CustomerFeed for feed ID %d and placeholder type %d\n'
         % (added_customer_feed['id'], added_customer_feed['placeholderTypes']))

if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, GMB_EMAIL_ADDRESS, GMB_ACCESS_TOKEN)
