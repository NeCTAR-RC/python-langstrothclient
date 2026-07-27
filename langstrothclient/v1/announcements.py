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

from nectarclient_lib import base


class AnnouncementUpdate(base.Resource):
    date_fields = ['time']

    def __repr__(self):
        return f"<AnnouncementUpdate {self.time}>"


class Announcement(base.Resource):
    """An announcement: an outage, a news post, or a hazard/security
    notice, discriminated by the `category` attribute.

    Unlike the legacy v1/outages resource there are no scheduled_*
    alias fields, `severity` is null for news, and nested updates
    carry no severity.
    """

    date_fields = ['start', 'end', 'planned_end']

    def __init__(self, manager, info, loaded=False, resp=None):
        super().__init__(manager, info, loaded, resp)
        raw_updates = self.updates
        self.updates = []
        for update in raw_updates:
            self.updates.append(AnnouncementUpdate(manager, update))

    def __repr__(self):
        return f"<Announcement {self.id}>"


class AnnouncementManager(base.BasicManager):
    # Read-only endpoint: list() and get() only.
    base_url = 'v1/announcements'
    resource_class = Announcement
