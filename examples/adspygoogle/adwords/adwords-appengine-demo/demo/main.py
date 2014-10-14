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
"""App Engine application module.

Configures the web application that will display the AdWords UI.
"""

__author__ = 'Mark Saniscalchi'

import webapp2

from demo import DEBUG
from views import *

app = webapp2.WSGIApplication([('/', InitView),
                               ('/showCredentials', ShowCredentials),
                               ('/updateCredentials', UpdateCredentials),
                               ('/showAccounts', ShowAccounts),
                               ('/showCampaigns', ShowCampaigns),
                               ('/addCampaign', AddCampaign),
                               ('/showAdGroups', ShowAdGroups),
                               ('/addAdGroup', AddAdGroup),
                               ('/showBudget', ShowBudget),
                               ('/updateBudget', UpdateBudget)],
                              debug=DEBUG)