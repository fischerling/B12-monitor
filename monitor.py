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

from gyms import GYMS


def get_html_js(gym_url) -> str:
    """Retrieve, execute js, render oand return the html of the gym's website

    To execute the javascript of the website pyppeteer is used a headless chromium instance.
    """

    from requests_html import HTMLSession  # pylint: disable=import-outside-toplevel

    with HTMLSession() as session:
        resp = session.get(gym_url)

        # Run JavaScript code on webpage
        resp.html.render()
        html = resp.html.html
        resp.close()

        return html


def get_html_nojs(gym_url) -> str:
    """Retrieve the html of the gym's website using requests"""
    import requests  # pylint: disable=import-outside-toplevel

    res = requests.get(gym_url)
    res.raise_for_status()

    return res.text


def get_html(gym_url, needs_js=False) -> str:
    """Retrieve the html of the gym's website"""

    if needs_js:
        return get_html_js(gym_url)

    return get_html_nojs(gym_url)


def extract_free_slots(html: str, gym_re) -> int:
    """Extract the free slots from the B12 website's html"""
    free_slots_re = re.compile(gym_re)
    match = free_slots_re.search(html)
    if not match:
        raise RuntimeError('Could not find the free slots')
    return int(match.group(1))


def is_gym_open(gym_opening_hours, now: datetime) -> bool:
    """Check if the gym is open"""
    opening_hours = [[time.fromisoformat(t) for t in oh] for oh in gym_opening_hours]

    weekday = now.weekday()
    hours_today = opening_hours[weekday]

    time_now = now.time()

    return hours_today[0] <= time_now < hours_today[1]


def print_free_slots(gym_name: str):
    """Print the current time and the free slots in the gym if it is actually open"""
    gym = GYMS[gym_name]

    now = datetime.now()
    if not is_gym_open(gym['opening_hours'], now):
        return

    html = get_html(gym['url'], needs_js=gym.get('needs_js', False))
    free_slots = extract_free_slots(html, gym['re'])
    data_suffix = '%' if 'percentage' in gym else ''
    print(f'{now.isoformat()}, {free_slots}{data_suffix}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gym', default='B12', help='Gym to monitor free slots')
    args = parser.parse_args()

    print_free_slots(args.gym)
