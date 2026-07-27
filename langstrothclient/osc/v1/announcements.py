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

import logging

from nectarclient_lib import exceptions
from osc_lib.command import command
from osc_lib import utils as osc_utils


class ListAnnouncements(command.Lister):
    """List announcements (outages, news, notices)."""

    log = logging.getLogger(__name__ + '.ListAnnouncements')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--category',
            metavar='<category>',
            choices=['outage', 'news', 'notice'],
            help='Only list announcements of this category',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.nectar_ops
        filters = {}
        if parsed_args.category:
            filters['category'] = parsed_args.category
        announcements = client.announcements.list(**filters)
        columns = [
            'id',
            'category',
            'title',
            'status_display',
            'severity_display',
            'start',
            'end',
        ]
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in announcements),
        )


class AnnouncementCommand(command.ShowOne):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of announcement'))
        return parser


class ShowAnnouncement(AnnouncementCommand):
    """Show announcement details."""

    log = logging.getLogger(__name__ + '.ShowAnnouncement')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.nectar_ops
        try:
            announcement = client.announcements.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(announcement.to_dict())
