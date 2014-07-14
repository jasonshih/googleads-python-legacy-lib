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

"""This example demonstrates how to authorize and configure an AdWordsClient."""

__author__ = 'api.msaniscalchi@gmail.com (Mark Saniscalchi)'

import sys

from adspygoogle import AdWordsClient
from oauth2client import client

CLIENT_CUSTOMER_ID = 'INSERT_CLIENT_CUSTOMER_ID_HERE'
CLIENT_ID = 'INSERT_CLIENT_ID_HERE'
CLIENT_SECRET = 'INSERT_CLIENT_SECRET_HERE'
SCOPE = 'https://www.googleapis.com/auth/adwords'
USER_AGENT = 'INSERT_USER_AGENT_HERE'
DEVELOPER_TOKEN = 'INSERT_DEVELOPER_TOKEN_HERE'


def main(client_customer_id, client_id, client_secret, developer_token, scope,
         user_agent):
  """Retrieve credentials and create an AdWordsClient.

  Args:
    client_customer_id: Your client customer id
    client_id: Your client id retrieved from the Google Developers Console.
    client_secret: Your client secretretrieved from the Google Developers
                   Console.
    developer_token: Your developer token.
    scope: Scope used for authorization.
    user_agent: A semi-unique string identifying this client.
  """
  flow = client.OAuth2WebServerFlow(
      client_id=client_id,
      client_secret=client_secret,
      scope=[scope],
      user_agent=user_agent,
      redirect_uri='urn:ietf:wg:oauth:2.0:oob')

  authorize_url = flow.step1_get_authorize_url()

  print ('Log into the Google Account you use to access your AdWords account'
         'and go to the following URL: \n%s\n' % (authorize_url))
  print 'After approving the token enter the verification code (if specified).'
  code = raw_input('Code: ').strip()

  try:
    credential = flow.step2_exchange(code)
  except client.FlowExchangeError, e:
    print 'Authentication has failed: %s' % e
    sys.exit(1)
  else:
    print ('OAuth 2.0 authorization successful!\n\n'
           'Your access token is:\n %s\n\nYour refresh token is:\n %s\n'
           % (credential.access_token, credential.refresh_token))

  # Create an AdWordsClient
  try:
    AdWordsClient(headers={
                              'clientCustomerId': client_customer_id,
                              'developerToken' : developer_token,
                              'oauth2credentials' : credential,
                              'userAgent' : user_agent
                          })

    print 'Successfully created AdWordsClient!'
  except Exception, e:
    print 'Failed to create AdWordsClient with error:\n %s' % e


if __name__ == '__main__':
  main(CLIENT_CUSTOMER_ID, CLIENT_ID, CLIENT_SECRET, DEVELOPER_TOKEN, SCOPE,
       USER_AGENT)