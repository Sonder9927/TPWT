# TPWT
---
## info
Dual plane wave phase velocity inversion in SH area.

Here is my backup.

This only records the form of the data,
the processing flow, some automated scripts that
process the data in the flow,
and some flashes of light.

Not public yet.
## DATA
### Raw Data
Seismic data from stations in the area.

My first-hand data is in `.miniseed` format.

### Preprocessing
Use `'sac'` to process and finally get only Z component, filtered 20-150s, 1Hz `.sac` data.
### Cut by event
I need to cut data by events from 30$\degree$ to 120$\degree$ and only need data within 3 hours after the earthquakes.

1. I download event catalog from [Search Earthquake Catalog](https://earthquake.usgs.gov/earthquakes/search/).

- Basic Options: 
  - Magnitude Minimum: 5.5

- Advanced Options:
  - Circle:
    - la:
    - lo:
    - km:
  - Event Type:
    - earthquakes: Earthquake
  - Output Options: CSV

So I get 120$\degree$ and 30$\degree$ event files in format `.csv` .

2. I use Python to treat the two event files. Code in `evt.ipynb`.

Then I will get 3 files:
  - event.cat: This will be used to cut event. Format is:

    `2021/12/30,13:13:17`
  - event_14.lst: This will be used in `01.bash`. Format is:

    `20211230131317 125.2498  -0.0798 5.5`
  - event_14_depth.cat: This will be used in `batch_sacfile_ch.py`. Format is:

    `20211230131317 125.2498  -0.0798 42.0`

Now I have `.sac` data files and `event.cat` file. I can cut data by events.

I will get some folders named `20211230131317` in which there are some `.sac` files.

And those folders are in the `Out` set by me.

### Sac File Rename and Modify Head File

Now I'm in `Out`.I will use:
- event_14_depth.cat: event lo la dp
- station_el.cat: station lo la el

I will add `evla evlo evdp stlo stla stel` to the head file which will automatically calculate `dist`
and change naming format of the sac files to be `eventtime.station.*.sac`.

`bash sac_ch_rename.sh`

Now sac files will change from `XX.station.00.XXZ.X.eventtime.sac`
to `eventtime.station.XXZ.sac`.And `dist` will appear in head file.

At this point, my data preparation is basically complete.
## 01.bash

Generate reference phase velocities for each pair of event and station, 
then extract dispersion curves for each sac file.

Prepare files:
- event_14.lst: event_14-digit lo la ma
- station.lst: station lo la

`bash 01.bash`

## 01.bash

---
