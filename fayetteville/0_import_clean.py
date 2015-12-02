import pandas as pd
import stateplane as sp
import numpy as np
import os, requests, zipfile, StringIO
import re

# get url
r = requests.get('https://s3-us-west-2.amazonaws.com/openpolicingdata/Fayetteville-11-09-15.xls.zip')
z = zipfile.ZipFile(StringIO.StringIO(r.content))

# create dirs and extract fayetteville file
tmpdir = os.path.join(os.getcwd(), 'temp')
os.mkdir(tmpdir)
f = z.namelist()[0]
z.extract(f, tmpdir)
df = pd.read_excel(os.path.join(tmpdir, f), sheetname=[0,1])
os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)

# # set path and import
# f = os.path.expanduser("~/Downloads/Fayetteville geolocational data.xls")
# dfs = pd.read_excel(f, sheetname=[0,1]) # dictionary of data frames
# df = pd.concat(dfs, ignore_index=True) # stack

# convert stateplane coords to lat long
latlon = df[['geox', 'geoy']].apply(lambda x: sp.to_latlon(x['geox']/100*0.3048,
  x['geoy']/100*0.3048, epsg='2264'), axis=1) # convert
lat = pd.Series([v[0] for v in latlon])
lon = pd.Series([v[1] for v in latlon])
latlon = pd.concat([lat, lon], axis = 1)
latlon.columns = [u'lat', u'lon']
df = pd.concat([df, latlon], axis = 1)

# change column names and remove odd values
df.columns = [x.lower() for x in df.columns]
rx = re.compile('\W+') # get all nonnumeric values (including spaces)
df.columns = [rx.sub('_', v) for v in df.columns] # all spaces to underscores

# FIX errors in 'state'
df.state = 'NC'

# change all nonnumeric values to strings
## code from http://stackoverflow.com/questions/20670370/pandas-and-unicode
types = df.apply(lambda x: pd.lib.infer_dtype(x.values))

for col in types[(types=='unicode') | (types=='mixed')].index:
  df[col] = df[col].astype(str)

# export
df.to_csv('/Users/dnoriega/Dropbox/codefordurham/fayetteville.csv', index=False)

