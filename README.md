# B12 Monitor

Collect and visualize the free slot of B12 and other climbing gym.

## Requirements

* python3
* matplotlib
* numpy
* [requests] if no javascript is needed
* [requests_html] if javascript is needed

## Usage

To collect the free slots from the B12 website and store them in a file run:

`./monitor.py > free_slots.csv`

To monitor the free slots over time use your shell:

```bash
while true
do
	./monitor.py
	sleep 300 # sleep for 5 minutes
done > free_slots.csv
```

To generate a heatmap in `free\_slots.png` from the collected data run:

`./plot.py free_slots.csv`

## Supported gyms

The current default gym is the B12 in Tuebingen because this is the gym I am
the most interested in.
But some other gyms are supported too.
Available gyms are defined in `gyms.py`.
Included Configurations:
* B12 (Tuebingen)
* Steinbock (Erlangen)
* DAV Bergwelt (Erlangen)
* Boulderwelt Ost (Muenchen)

A gym configuration consists of the url were they show their currently available
free slots, a regex how to extract the free slots from the retrieved html as well
as the opening hours.

## Collected Data

Plots of the all gyms I am monitoring can be found at:
[muhq.space/gym-heatmap.html](https://muhq.space/gym-heatmap.html).

## Similar projects

[B12 data mining](https://github.com/jnsbck/B12_data_mining) by Jonas Beck

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
