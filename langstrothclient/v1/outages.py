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

import json

from nectarclient_lib import base

from langstrothclient import constants


class OutageUpdate(base.Resource):

    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
    date_fields = ['time']

    def __repr__(self):
        return "<OutageUpdate %s>" % self.time


class Outage(base.Resource):

    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
    date_fields = ['scheduled_start', 'scheduled_end']

    def __init__(self, manager, info, loaded=False, resp=None):
        super().__init__(manager, info, loaded, resp)
        raw_updates = self.updates
        self.updates = []
        for update in raw_updates:
            self.updates.append(OutageUpdate(manager, update))

    def __repr__(self):
        return "<Outage %s>" % self.id

    @property
    def severity(self):
        return (self.updates[-1].severity if self.updates
                else self.scheduled_severity)

    @property
    def severity_display(self):
        return constants.SEVERITY_DISPLAY.get(self.severity, "Unknown")

    @property
    def scheduled_display(self):
        return ("Cancelled" if self.cancelled
                else "Scheduled" if self.scheduled
                else "Unscheduled")

    @property
    def status_display(self):
        if self.updates:
            return constants.STATUS_DISPLAY.get(
                self.updates[-1].status, "Not Started")
        return "Not Started"

    @property
    def start(self):
        if self.updates:
            return self.updates[0].time
        else:
            return None

    @property
    def end(self):
        if (self.updates
            and self.updates[-1].status in (constants.COMPLETED,
                                            constants.RESOLVED)):
            return self.updates[-1].time
        else:
            return None


class OutageManager(base.BasicManager):

    base_url = 'v1/outages'
    resource_class = Outage

    def update(self, outage_id, **kwargs):
        data = json.dumps(kwargs)
        return self._update(f"/{self.base_url}/{outage_id}/", data=data)
