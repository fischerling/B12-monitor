#!/usr/bin/env python3
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
"""Periodically scrape the B12 website and extract the free slots"""

from datetime import datetime, time
import re
from time import sleep

from requests_html import HTMLSession


def render() -> str:
    """Retrieve, render and return the complete html of the B12 website"""
    session = HTMLSession()

    b12_url = 'http://b12-tuebingen.de/'
    resp = session.get(b12_url)

    # Run JavaScript code on webpage
    resp.html.render()
    html = resp.html.html
    resp.close()

    return html


def extract_free_slots(html: str) -> int:
    """Extract the free slots from the B12 website's html"""
    trafficlight_text_re = re.compile(
        r'<div class="status_text">(\d*) freie Plätze\s*</div>')
    match = trafficlight_text_re.search(html)
    if not match:
        raise RuntimeError('Could not find the traffic light status text')
    return int(match.group(1))


def is_b12_open(now: datetime) -> bool:
    """Check if the B12 is open"""
    opening_hours_str = (('09:30', '23:00'), ('09:30', '23:00'),
                         ('08:30', '23:00'), ('12:30', '23:00'),
                         ('09:30', '23:00'), ('10:00', '22:00'), ('10:00',
                                                                  '21:30'))

    opening_hours = [[time.fromisoformat(t) for t in oh]
                     for oh in opening_hours_str]

    weekday = now.weekday()
    hours_today = opening_hours[weekday]

    time_now = now.time()

    return hours_today[0] >= time_now <= hours_today[1]


def print_free_slots():
    """Print the current time and the free slots if the B12 is actually open"""
    now = datetime.now()
    if not is_b12_open(now):
        return

    html = render()
    free_slots = extract_free_slots(html)
    print(f'{now.isoformat()}, {free_slots}')


if __name__ == '__main__':
    while True:
        print_free_slots()
        # sleep 5 min
        sleep(60 * 5)
