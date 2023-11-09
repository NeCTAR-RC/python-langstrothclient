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

from osc_lib.command import command
from osc_lib import utils as osc_utils

from langstrothclient import exceptions


class ListOutages(command.Lister):
    """List outages."""

    log = logging.getLogger(__name__ + '.ListUsers')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.outage
        outages = client.outages.list()
        columns = ['id', 'title', 'status', 'severity', 'start', 'end']
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in outages)
        )


class OutageCommand(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(OutageCommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('ID of outage')
        )
        return parser


class ShowOutage(OutageCommand):
    """Show outage details."""

    log = logging.getLogger(__name__ + '.ShowOutage')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.outage
        try:
            user = client.outages.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(user.to_dict())
