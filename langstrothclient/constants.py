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

# Outage Status
STARTED = 'S'
INVESTIGATING = 'IN'
IDENTIFIED = 'ID'
PROGRESSING = 'P'
FIXED = 'F'
RESOLVED = 'R'
COMPLETED = 'C'
STATUS_DISPLAY = {
    STARTED: 'Started',
    INVESTIGATING: 'Investigating',
    IDENTIFIED: 'Identified',
    PROGRESSING: 'Progressing',
    FIXED: 'Fixed',
    RESOLVED: 'Resolved',
    COMPLETED: 'Completed'
}

# Outage Severity
MINIMAL = 1
SIGNIFICANT = 2
SEVERE = 3
SEVERITY_DISPLAY = {
    MINIMAL: 'Minimal',
    SIGNIFICANT: 'Significant',
    SEVERE: 'Severe'
}
