# B12 Monitor

Collect and visualize the free slot of B12 climbing gym.

## Requirements

* python3
* requests_html
* matplotlib
* numpy

## Usage

To periodically collect the free slots from the B12 website and store them in a file run:

`./monitor.py > free_slots.csv`

To generate a heatmap in free\_slots.png using the collected data run:

`./plot.py free_slots.csv`

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
