#Ubuntu 14.04:

In order to run this script, install in this order from the command line:

```bash
$ apt-get install libgeos-dev

$ apt-get install libgdal-dev

$ pip install stateplane
```

This script was written to convert GIS coordinates from the Fayetteville Police Department that uses the State Plane (NC) System. 

The python package stateplane is used to accomplish this. Stateplane supports mesurements in meters, so we convert the geox and geoy datafeilds to meters.

Additionally, the process used to export the Fayetteville data apparently removed a decimal point from the data, so the feild required being dividing by 100 to have the correct number of digits.

In this case a street intersection was also provided with the geox and geoy coordinates, and we were able to cross reference these and check for accuracy.
