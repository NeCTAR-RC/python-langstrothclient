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

import datetime

from langstrothclient.tests.unit import utils
from langstrothclient.tests.unit.v1 import fakes
from langstrothclient.v1 import announcements


class AnnouncementsTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_announcement_list(self):
        al = self.cs.announcements.list()
        self.cs.assert_called('GET', '/v1/announcements/')
        for a in al:
            self.assertIsInstance(a, announcements.Announcement)
        self.assertEqual(3, len(al))
        self.assertEqual(
            ['outage', 'notice', 'news'], [a.category for a in al]
        )

    def test_announcement_list_category_filter(self):
        al = self.cs.announcements.list(category='news')
        self.assertEqual(1, len(al))
        self.assertEqual('news', al[0].category)

    def test_announcement_get(self):
        a = self.cs.announcements.get(201)
        self.cs.assert_called('GET', '/v1/announcements/201/')
        self.assertIsInstance(a, announcements.Announcement)
        self.assertEqual(201, a.id)

    def test_attrs(self):
        a = self.cs.announcements.get(201)
        self.assertEqual('outage', a.category)
        self.assertIsInstance(a.start, datetime.datetime)
        self.assertIsInstance(a.end, datetime.datetime)
        self.assertIsInstance(a.planned_end, datetime.datetime)
        self.assertIsInstance(a.updates[0].time, datetime.datetime)
        self.assertEqual(3, a.severity)
        self.assertEqual('Severe', a.severity_display)
        self.assertEqual('Completed', a.status_display)
        # Clean contract: no scheduled_* aliases on this endpoint.
        self.assertFalse(hasattr(a, 'scheduled_start'))

    def test_news_attrs(self):
        a = self.cs.announcements.get(203)
        self.assertEqual('news', a.category)
        self.assertIsNone(a.severity)
        self.assertIsNone(a.severity_display)
        self.assertIsNone(a.end)
        self.assertIsNone(a.planned_end)
        self.assertEqual('Published', a.status_display)
        self.assertEqual([], a.updates)
        self.assertIsInstance(a.start, datetime.datetime)
