# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

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

df0 = pd.read_excel(os.path.join(tmpdir, f), sheetname=0)
df1 = pd.read_excel(os.path.join(tmpdir, f), sheetname=1)

frames = [df0, df1]

df = pd.concat(frames)

df = df.set_index('TSR ID')

os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)

# # set path and import

# convert stateplane coords to lat long
df[['geox', 'geoy']] = df[['geox', 'geoy']].apply(lambda x: sp.to_latlon(x['geox']/100*0.3048,
  x['geoy']/100*0.3048, epsg='2264'), axis=1) # convert

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
df.to_csv(os.path.join(os.getcwd(), 'fayCSVdata.csv'), index=False)
print 'Check for fayCSVdata.csv in your current working directory'
