#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Settings and configuration for the unit tests."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))

from adspygoogle.dfp.DfpClient import DfpClient


HTTP_PROXY = None
SERVER_V201208 = 'https://ads.google.com'
SERVER_V201211 = 'https://ads.google.com'

TEST_VERSION_V201208 = True
TEST_VERSION_V201211 = True

VERSION_V201208 = 'v201208'
VERSION_V201211 = 'v201211'

client = DfpClient(path=os.path.join('..', '..', '..'))
