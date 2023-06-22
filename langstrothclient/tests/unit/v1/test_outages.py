#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from langstrothclient.v1 import outages

from langstrothclient.tests.unit import utils
from langstrothclient.tests.unit.v1 import fakes


class OutagesTest(utils.TestCase):

    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_outage_list(self):
        ol = self.cs.outages.list()
        self.cs.assert_called('GET', '/v1/outages/')
        for o in ol:
            self.assertIsInstance(o, outages.Outage)
        self.assertEqual(3, len(ol))

    def test_outage_get(self):
        o = self.cs.outages.get(123)
        self.cs.assert_called('GET', '/v1/outages/123/')
        self.assertIsInstance(o, outages.Outage)
        self.assertEqual(123, o.id)
