import pandas as pd
import stateplane as sp
import numpy as np
import os, requests, zipfile, StringIO, ssl
import re
import json as json
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()


print 'This will take a little while.'
#get url
r = requests.get('https://s3-us-west-2.amazonaws.com/openpolicingdata/Fayetteville-11-09-15.xls.zip')
z = zipfile.ZipFile(StringIO.StringIO(r.content))

# create dirs and extract fayetteville file
tmpdir = os.path.join(os.getcwd(), 'temp')
os.mkdir(tmpdir)
f = z.namelist()[0]
z.extract(f, tmpdir)

df0 = pd.read_excel(os.path.join(tmpdir, f), sheetname=0)
df1 = pd.read_excel(os.path.join(tmpdir, f), sheetname=1)

frames = [df0, df1]

df = pd.concat(frames)

df = df.set_index('TSR ID')
df.head()

os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)

# convert stateplane coords to lat long
# note this raw data was missing a decimal point, hence the dividing by 100
df[['geox', 'geoy']] = df[['geox', 'geoy']].apply(lambda x: sp.to_latlon(x['geox']/100*0.3048,
  x['geoy']/100*0.3048, epsg='2264'), axis=1) # convert
df.head()

# change column names and remove odd values
df.columns = [x.lower() for x in df.columns]
rx = re.compile('\W+') # get all nonnumeric values (including spaces)
df.columns = [rx.sub('_', v) for v in df.columns] # all spaces to underscores

# create seperate year, and month columns
df['year'] = pd.DatetimeIndex(df['stopdate']).year
df['month'] = pd.DatetimeIndex(df['stopdate']).month

# FIX errors in 'state'
df.state = 'NC'

# change all nonnumeric values to strings
## code from http://stackoverflow.com/questions/20670370/pandas-and-unicode
types = df.apply(lambda x: pd.lib.infer_dtype(x.values))

for col in types[(types=='unicode') | (types=='mixed')].index:
  df[col] = df[col].astype(str)

#following function thanks to Geoff Boeing @ http://geoffboeing.com/2015/10/exporting-python-data-geojson/

def df_to_geojson(df, properties, lat='geox', lon='geoy'):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

cols = ['sex', 'race', 'ethnic', 'age', 'street', 'year', 'month']
geojson = df_to_geojson(df, cols)

output_filename = 'FayGeoData.json'
with open(output_filename, 'wb') as output_file:
  # output_file.write('var dataset = ')
    json.dump(geojson, output_file, indent=None) ## indent=None creates a smaller file. 
                                                 ## Use indent=2 for human readable format
    print 'check your current working directory for FayGeoData.js'
   

