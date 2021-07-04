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

import argparse
from datetime import datetime, time
import re
from time import sleep

from requests_html import HTMLSession

from gyms import GYMS


def render(gym_url) -> str:
    """Retrieve, render and return the complete html of the B12 website"""
    with HTMLSession() as session:
        resp = session.get(gym_url)

        # Run JavaScript code on webpage
        resp.html.render()
        html = resp.html.html
        resp.close()

        return html


def extract_free_slots(html: str, gym_re) -> int:
    """Extract the free slots from the B12 website's html"""
    free_slots_re = re.compile(gym_re)
    match = free_slots_re.search(html)
    if not match:
        raise RuntimeError('Could not find the free slots')
    return int(match.group(1))


def is_gym_open(gym_opening_hours, now: datetime) -> bool:
    """Check if the gym is open"""
    opening_hours = [[time.fromisoformat(t) for t in oh]
                     for oh in gym_opening_hours]

    weekday = now.weekday()
    hours_today = opening_hours[weekday]

    time_now = now.time()

    return hours_today[0] <= time_now <= hours_today[1]


def print_free_slots(gym_name: str):
    """Print the current time and the free slots in the gym if it is actually open"""
    gym = GYMS[gym_name]

    now = datetime.now()
    if not is_gym_open(gym['opening_hours'], now):
        return

    html = render(gym['url'])
    free_slots = extract_free_slots(html, gym['re'])
    print(f'{now.isoformat()}, {free_slots}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',
                        '--interval',
                        default=60 * 5,
                        help='time interval between extraction runs')
    parser.add_argument('-g',
                        '--gym',
                        default='B12',
                        help='Gym to monitor free slots')
    args = parser.parse_args()

    while True:
        print_free_slots(args.gym)
        sleep(args.interval)
