# requirements for [stateplane](https://github.com/fitnr/stateplane) package
Follow the instructions to download the repository and run

```
python setup.py install
```

It may fail and require that you have `goes` and `gdal` installed.

```
pip install geos
pip install gdal
```

Mac OS X 10.10 users, you *cannot use the system* python to install as 10.10 does not allow system level installs. You will have to run a separate python framework.