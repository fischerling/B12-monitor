# Copyright 2021 Florian Fischer

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Configuration for the supported climbing gym web pages"""

GYMS = {
    'B12': {
        'url': ('https://111.webclimber.de/de/trafficlight?callback=WebclimberTrafficlight.'
                'insertTrafficlight&key=184xNhv6RRU7H2gVg8QFyHCYxym8DKve&hid=111&container='
                'trafficlightContainer&type=&area='),
        'needs_js': False,
        're': r"<div class='status_text'>(\d+) freie Pl.*</div>",
        'opening_hours': (
            ('09:30', '23:00'), ('09:30', '23:00'), ('08:30', '23:00'), ('12:30', '23:00'),
            ('09:30', '23:00'), ('10:00', '22:00'), ('10:00', '21:30'))
    },
    'BergWeltErlangen': {
        'url': ('https://www.boulderado.de/boulderadoweb/gym-clientcounter/index.php?mode=get&'
                'token=eyJhbGciOiJIUzI1NiIsICJ0eXAiOiJKV1QifQ.eyJjdXN0b21lciI6IkRBVkVybGFuZ2VuM'
                'jMyMDIwIn0.Fr3KR0obdp_aYzCIclQTMZr0dVIxT0bfyUVODU_u64M'),
        'needs_js': False,
        're': r'<div class="freecounter-content"><span data-value="\d+">(\d+)</span></div>',
        'opening_hours': (
            ('10:30', '22:00'), ('10:30', '22:00'), ('10:30', '22:00'), ('10:30', '22:00'),
            ('10:30', '22:00'), ('09:00', '20:00'), ('09:00', '20:00'))
    }
}
