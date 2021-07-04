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
        'url':
        'http://b12-tuebingen.de/',
        're':
        r'<div class="status_text">(\d+) freie Plätze\s*</div>',
        'opening_hours':
        (('09:30', '23:00'), ('09:30', '23:00'), ('08:30', '23:00'),
         ('12:30', '23:00'), ('09:30', '23:00'), ('10:00', '22:00'), ('10:00',
                                                                      '21:30'))
    },
    'BergWeltErlangen': {
        'url':
        'https://www.boulderado.de/boulderadoweb/gym-clientcounter/index.php?mode=get&token=eyJhbGciOiJIUzI1NiIsICJ0eXAiOiJKV1QifQ.eyJjdXN0b21lciI6IkRBVkVybGFuZ2VuMjMyMDIwIn0.Fr3KR0obdp_aYzCIclQTMZr0dVIxT0bfyUVODU_u64M',
        're':
        r'<div class="freecounter-content"><span data-value="\d+">(\d+)</span></div>',
        'opening_hours':
        (('10:30', '22:00'), ('10:30', '22:00'), ('10:30', '22:00'),
         ('10:30', '22:00'), ('10:30', '22:00'), ('09:00', '20:00'), ('09:00',
                                                                      '20:00'))
    }
}
