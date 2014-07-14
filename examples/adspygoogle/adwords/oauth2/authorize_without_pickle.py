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

"""This example will demonstrate how to step through the OAuth2 flow manually.

This example is meant to be run from the command line and requires a user to
provide a value for the CLIENT_ID and CLIENT_SECRET constants. This example
doesn't use information provided by adwords_api_config.pkl.
"""

__author__ = 'api.msaniscalchi@gmail.com (Mark Saniscalchi)'

import sys

from oauth2client import client


CLIENT_ID = 'INSERT_CLIENT_ID_HERE'
CLIENT_SECRET = 'INSERT_CLIENT_SECRET_HERE'
ADWORDS_SCOPE = 'https://www.googleapis.com/auth/adwords'


def main(client_id, client_secret, scope):
  """Retrieve and display a refresh token.

  Args:
    client_id: retrieved from the Google Developers Console.
    client_secret: retrieved from the Google Developers Console.
    scope: Scope used for authorization.
  """
  flow = client.OAuth2WebServerFlow(
      client_id=client_id,
      client_secret=client_secret,
      scope=[scope],
      user_agent='Ads Python Client Library',
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
           'Your access token is:\n %s\n\nYour refresh token is:\n %s'
           % (credential.access_token, credential.refresh_token))


if __name__ == '__main__':
  main(CLIENT_ID, CLIENT_SECRET, ADWORDS_SCOPE)