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
"""Plot a heat map using scrapped free slots from the B12 website"""

import argparse
import csv
from datetime import datetime, date, time, timedelta
import math
from pathlib import Path
from typing import List, Tuple, Optional

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class RunningAverage:
    """Simple convenience class representing a running average

    https://en.wikipedia.org/wiki/Moving_average
    """
    def __init__(self):
        self.number = 0
        self.average = 0.0

    def __add__(self, i: float):
        """Add a value to the running average"""
        self.number += 1
        self.average += (i - self.average) / self.number
        return self

    def get_avg(self) -> float:
        """Return the current average or np.nan if no data were added"""
        if self.number == 0:
            return np.nan
        return self.average

    def __int__(self):
        """Return an integer representation of the current average"""
        return int(self.get_avg())

    def __float__(self):
        """Return the current average"""
        return self.get_avg()


def __add_minutes_to_time(start_time: time, minutes: int) -> time:
    """add minutes to a time by converting to datetime and back"""
    return (datetime.combine(date.today(), start_time) + timedelta(minutes=minutes)).time()


WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

OPENING_HOURS = (('09:30', '23:00'), ('09:30', '23:00'), ('08:30', '23:00'), ('12:30', '23:00'),
                 ('09:30', '23:00'), ('10:00', '22:00'), ('10:00', '21:30'))

PLOT_DURATION = (time.fromisoformat('09:30'), time.fromisoformat('23:00'))
SLOT_DURATION = timedelta(minutes=30)


def calc_interval(time_point: time) -> int:
    """Calculate the integer index of the interval this time points belongs to"""
    first_slot = timedelta(hours=PLOT_DURATION[0].hour, minutes=PLOT_DURATION[0].minute)
    delta = timedelta(hours=time_point.hour, minutes=time_point.minute) - first_slot
    slot_idx = int(delta / SLOT_DURATION)
    return slot_idx


def generate_slots() -> Tuple[List[Tuple[time, time]], List[str]]:
    """generate relevant time slots and y-ticks"""
    slots = []
    y_labels = []
    slot = PLOT_DURATION[0]
    while slot < PLOT_DURATION[1]:
        next_slot = __add_minutes_to_time(slot, 30)
        slots.append((slot, next_slot))
        y_labels.append(f'{slot.isoformat("minutes")} - {next_slot.isoformat("minutes")}')
        slot = next_slot

    return slots, y_labels


def prepare_heatmap(data_path: str, intervals: List[Tuple[time, time]]) -> List[List[float]]:
    """parse csv data into a N,M matrix containing the average free slots in each interval

    N: slots
    M: weekdays
    """

    with open(data_path, 'r', encoding='utf-8') as data_file:
        reader = csv.reader(data_file, delimiter=',')
        data = list(reader)

    # prepare the heat map data
    # x-axis are our weekdays
    # y-axis are 30 min time intervals
    # each 30 minute slot is represented by a running average of
    # all collected data points during this slot
    avgs = [[RunningAverage() for _ in range(len(WEEKDAYS))] for _ in range(len(intervals))]

    for data_point in data:
        time_point = datetime.fromisoformat(data_point[0])
        free_slots = float(data_point[1])

        weekday = time_point.weekday()

        interval = calc_interval(time_point.time())

        interval_avg = avgs[interval][weekday]

        interval_avg += free_slots

    return [[float(avg) for avg in weekday] for weekday in avgs]


def plot(data_path: str, outfile: Optional[str]):
    """plot a heat map containing the free slots scraped from the b12 website"""

    slots, y_labels = generate_slots()

    free_slots = prepare_heatmap(data_path, slots)

    fig, axis = plt.subplots()

    cmap = matplotlib.colors.ListedColormap(
        ['darkred', 'red', 'darkorange', 'orange', 'olive', 'darkolivegreen', 'green'])
    cmap.set_bad(color='grey')

    axis.imshow(free_slots, cmap=cmap, aspect='auto')

    axis.set_xticks(np.arange(len(WEEKDAYS)))
    axis.set_xticklabels(WEEKDAYS)
    plt.setp(axis.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    axis.set_yticks(np.arange(len(slots)))
    axis.set_yticklabels(y_labels)

    # Add free slots text
    for i in range(len(slots)):
        for j in range(len(WEEKDAYS)):
            data_point = free_slots[i][j]
            if math.isnan(data_point):
                continue
            axis.text(j, i, int(data_point), ha="center", va="center", color="w")

    axis.set_title("Free slots over time")

    out = outfile or Path(data_path).with_suffix('.png')
    fig.savefig(out, bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', help='csv input file')
    parser.add_argument('-o', '--outfile', nargs='?', const=None, help='output file')

    args = parser.parse_args()
    plot(args.data_file, args.outfile)
