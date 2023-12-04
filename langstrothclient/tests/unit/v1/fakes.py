#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import re
from unittest import mock

from six.moves.urllib import parse

from langstrothclient import client as base_client
from langstrothclient.tests.unit import fakes
from langstrothclient.tests.unit import utils
from langstrothclient.v1 import client
from langstrothclient.v1 import outages


# regex to compare callback to result of get_endpoint()
# checks version number (vX or vX.X where X is a number)
# and also checks if the id is on the end
ENDPOINT_RE = re.compile(
    r"^get_http:__langstroth_api:8774_v\d(_\d)?_\w{32}$")

# accepts formats like v2 or v2.1
ENDPOINT_TYPE_RE = re.compile(r"^v\d(\.\d)?$")

# accepts formats like v2 or v2_1
CALLBACK_RE = re.compile(r"^get_http:__langstroth_api:8774_v\d(_\d)?$")

generic_updates = [
    {'content': 'We are starting now ...',
     'time': '2023-09-14T10:39:51+10:00',
     'status': 'S',
     'severity': 3},
    {'content': 'It is finished.',
     'time': '2023-10-03T16:27:52+11:00',
     'status': 'C',
     'severity': 3}
]

generic_outage = {
    "title": "The sky is falling",
    "id": 123,
    "description": "The sky is falling all over the world. We are doomed.",
    "scheduled": True,
    "cancelled": False,
    "scheduled_start": '2023-09-14T10:38:26+10:00',
    "scheduled_end": '2023-09-22T17:00:00+10:00',
    "scheduled_severity": 3,
    "severity": 3,
    "severity_display": "Severe",
    "scheduled_display": "Scheduled",
    "status_display": 'Completed',
    "start": '2023-09-14T10:39:51+10:00',
    "end": '2023-10-03T16:27:52+10:00',
    "updates": generic_updates,
}


class FakeClient(fakes.FakeClient, client.Client):

    def __init__(self, *args, **kwargs):
        client.Client.__init__(self, session=mock.Mock())
        self.http_client = FakeSessionClient(**kwargs)
        self.outages = outages.OutageManager(self.http_client)


class FakeSessionClient(base_client.SessionClient):

    def __init__(self, *args, **kwargs):

        self.callstack = []
        self.visited = []
        self.auth = mock.Mock()
        self.session = mock.Mock()
        self.service_type = 'service_type'
        self.service_name = None
        self.endpoint_override = None
        self.interface = None
        self.region_name = None
        self.version = None
        self.auth.get_auth_ref.return_value.project_id = 'tenant_id'
        # determines which endpoint to return in get_endpoint()
        # NOTE(augustina): this is a hacky workaround, ultimately
        # we need to fix our whole mocking architecture (fixtures?)
        if 'endpoint_type' in kwargs:
            self.endpoint_type = kwargs['endpoint_type']
        else:
            self.endpoint_type = 'endpoint_type'
        self.logger = mock.MagicMock()

    def request(self, url, method, **kwargs):
        return self._cs_request(url, method, **kwargs)

    def _cs_request(self, url, method, **kwargs):
        # Check that certain things are called correctly
        if method in ['GET', 'DELETE']:
            assert 'data' not in kwargs
        elif method == 'PUT':
            assert 'data' in kwargs

        if url is not None:
            # Call the method
            args = parse.parse_qsl(parse.urlparse(url)[4])
            kwargs.update(args)
            munged_url = url.rsplit('?', 1)[0]
            munged_url = munged_url.strip('/').replace('/', '_')
            munged_url = munged_url.replace('.', '_')
            munged_url = munged_url.replace('-', '_')
            munged_url = munged_url.replace(' ', '_')
            munged_url = munged_url.replace('!', '_')
            munged_url = munged_url.replace('@', '_')
            munged_url = munged_url.replace('%20', '_')
            munged_url = munged_url.replace('%3A', '_')
            callback = "%s_%s" % (method.lower(), munged_url)

        if not hasattr(self, callback):
            raise AssertionError('Called unknown API method: %s %s, '
                                 'expected fakes method name: %s' %
                                 (method, url, callback))

        # Note the call
        self.visited.append(callback)
        self.callstack.append((method, url, kwargs.get('data'),
                               kwargs.get('params')))

        status, headers, data = getattr(self, callback)(**kwargs)

        r = utils.TestResponse({
            "status_code": status,
            "text": data,
            "headers": headers,
        })
        return r, data

    def get_v1_outages(self, **kwargs):
        outages = [
            {
                "title": "The sky is falling",
                "id": 123,
                "description": "The sky is falling all over the world",
                "scheduled": True,
                "cancelled": False,
                "scheduled_start": '2023-09-14T10:38:26+10:00',
                "scheduled_end": '2023-09-22T17:00:00+10:00',
                "scheduled_severity": 3,
                "updates": generic_updates,
            },
            {
                "title": "The sun is rising",
                "id": 124,
                "description": "Time to start your research.",
                "scheduled": True,
                "cancelled": False,
                "scheduled_start": '2023-09-14T10:38:26+10:00',
                "scheduled_end": '2023-09-22T17:00:00+10:00',
                "scheduled_severity": 3,
                "updates": [],
            },
            {
                "title": "It is raining",
                "id": 125,
                "description": "Lovely weather here in Seattle.",
                "scheduled": True,
                "cancelled": False,
                "scheduled_start": '2023-09-14T10:38:26+10:00',
                "scheduled_end": '2023-09-22T17:00:00+10:00',
                "scheduled_severity": 3,
                "updates": generic_updates,
            },
        ]
        return (200, {}, outages)

    def get_v1_outages_123(self, **kwargs):
        return (200, {}, generic_outage)
