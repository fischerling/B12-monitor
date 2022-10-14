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
import sys

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

SLOT_DURATION = timedelta(minutes=30)
Slot = Tuple[time, time]


def calc_interval(time_point: time, intervals: List[Slot]) -> int:
    """Calculate the integer index of the interval this time points belongs to"""
    first_slot = intervals[0]
    first_slot_start = timedelta(hours=first_slot[0].hour, minutes=first_slot[0].minute)
    delta = timedelta(hours=time_point.hour, minutes=time_point.minute) - first_slot_start
    slot_idx = int(delta / SLOT_DURATION)
    return slot_idx


DataPoint = Tuple[datetime, float]
Data = List[DataPoint]


def load_data(data_path: str) -> Optional[Tuple[Data, bool]]:
    """Load and parse csv data from data_path"""

    with open(data_path, 'r', encoding='utf-8') as data_file:
        reader = csv.reader(data_file, delimiter=',')
        data = list(reader)

    if not data:
        return None

    # Is the data given in percent?
    percentage = data[0][1].endswith('%')

    res = []
    for entry in data:
        time_point = datetime.fromisoformat(entry[0])

        if not percentage:
            # data are absolute free slots
            free_slots = float(entry[1])
        else:
            # data is load in percentage
            # flip it to get free slots in percentage
            free_slots = 100 - float(entry[1][:-1])

        res.append((time_point, free_slots))

    return res, percentage


def count_days_in_data(data: Data) -> int:
    """count and return the days in data

    Note: ths function expects data to be sorted.
    """
    days = 1
    cur_day = data[0][0].date()
    for time_point, _ in data:
        if time_point.date() > cur_day:
            days += 1
            cur_day = time_point.date()
    return days


def generate_slots(data: Data) -> Tuple[List[Slot], List[str]]:
    """generate relevant time slots and y-ticks"""

    # Find earliest and latest time_point in data
    earliest = data[0][0].time()
    latest = data[0][0].time()
    for datetime_point, _ in data:
        time_point = datetime_point.time()
        if time_point < earliest:
            earliest = time_point
        if time_point > latest:
            latest = time_point

    earliest = time(hour=earliest.hour, minute=earliest.minute)
    latest = time(hour=latest.hour, minute=latest.minute)

    slots = []
    y_labels = []
    slot = earliest
    while slot < latest:
        next_slot = __add_minutes_to_time(slot, 30)
        slots.append((slot, next_slot))
        y_labels.append(f'{slot.isoformat("minutes")} - {next_slot.isoformat("minutes")}')
        slot = next_slot

    return slots, y_labels


Map = List[List[float]]


def prepare_heatmap(data: Data, intervals: List[Slot]) -> Map:
    """parse data into a N,M matrix containing the average free slots in each interval

    N: slots
    M: weekdays
    """

    # prepare the heat map data
    # x-axis are our weekdays
    # y-axis are 30 min time intervals
    # each 30 minute slot is represented by a running average of
    # all collected data points during this slot
    avgs = [[RunningAverage() for _ in range(len(WEEKDAYS))] for _ in range(len(intervals))]

    for time_point, free_slots in data:
        weekday = time_point.weekday()

        interval = calc_interval(time_point.time(), intervals)

        interval_avg = avgs[interval][weekday]

        interval_avg += free_slots

    return [[float(avg) for avg in weekday] for weekday in avgs]


def plot(data_path: str, time_range: Optional[timedelta], outfile: Optional[str]):
    """plot a heat map containing the free slots scraped from the b12 website"""

    data, percentage = load_data(data_path) or (None, None)
    if not data:
        print(f'no data found in {data_path}', file=sys.stderr)
        sys.exit(1)

    if time_range:
        deadline = datetime.now() - time_range
        data = [data_point for data_point in data if data_point[0] >= deadline]
        if not data:
            print(f'no data newer than {deadline}', file=sys.stderr)
            sys.exit(0)

    slots, y_labels = generate_slots(data)

    free_slots = prepare_heatmap(data, slots)

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
    data_suffix = '%' if percentage else ''
    for i in range(len(slots)):
        for j in range(len(WEEKDAYS)):
            data_point = free_slots[i][j]
            if math.isnan(data_point):
                continue
            axis.text(j, i, f'{int(data_point)}{data_suffix}', ha="center", va="center", color="w")

    days = count_days_in_data(data)
    axis.set_title(f'Free slots over time (data of {days} days)')

    out = outfile or Path(data_path).with_suffix('.png')
    fig.savefig(out, bbox_inches='tight')


def main():
    """Main programm entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', help='csv input file')
    parser.add_argument('-o', '--outfile', nargs='?', const=None, help='output file')
    parser.add_argument('-w',
                        '--last-week',
                        action='store_true',
                        help='use only data of the last week')

    args = parser.parse_args()

    time_range = None
    if args.last_week:
        time_range = timedelta(weeks=1)

    plot(args.data_file, time_range, args.outfile)


if __name__ == '__main__':
    main()
