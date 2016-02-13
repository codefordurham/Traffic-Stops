#USES PYTHON 2.7

These scripts were written to convert GIS coordinates from the Fayetteville Police Department that uses the State Plane (NC) System.

xlsTOcsv.py takes the raw data from Fayetteville police dept., converts the GIS from stateplane system to degrees north/south, and east/west and then saves this as a .csv file

xlsTOgeoJSON.py takes the raw data from Fayetteville police dept., converts the GIS from stateplane system to degrees north/south, and east/west and then selects the new lat/lon feilds along with a selection of other demographic data and creates a geojson file with said information.

The python package stateplane is used to accomplish this. Stateplane supports mesurements in meters, so we convert the geox and geoy datafeilds to meters.

Additionally, the process used to export the Fayetteville data apparently removed a decimal point from the data, so the feild required being dividing by 100 to have the correct number of digits.

In this case a street intersection was also provided with the geox and geoy coordinates, and we were able to cross reference these and check for accuracy.

Currently, the raw data is downloaded each time the script is run into a temporary file which is deleted after the data is retreived. This is useful if the raw data is subject to change, however it is not the fastest if one anticipates running the script multiple times and don't expect the raw data to change.

##For Ubuntu 14.04:

In order to run either script, install in this order from the command line:

```bash

$ apt-get install python-pyasn1

$ pip install cryptography

$ apt-get install libgeos-dev

$ apt-get install libgdal-dev

$ pip install stateplane
```
# For mac OS

```
pip install geos
pip install gdal
```
Requirements for [stateplane](https://github.com/fitnr/stateplane) package
Follow the instructions to download the repository and run

```
python setup.py install

Mac OS X 10.10 users, you *cannot use the system* python to install as 10.10 does not allow system level installs. You will have to run a separate python framework.
Status API Training Shop Blog About Pricing
