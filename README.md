MetaSearch Catalogue Client QGIS Plugin
=======================================

[![Build Status](https://travis-ci.org/geopython/MetaSearch.png?branch=master)](https://travis-ci.org/geopython/MetaSearch)

MetaSearch is a QGIS plugin to interact with metadata catalogue services (CSW).

```
$ git clone https://github.com/geopython/MetaSearch.git
$ cd MetaSearch
# install development environment dependencies
$ pip install -r requirements-dev.txt
#
# install plugin dependencies
$ paver setup
#
# install plugin to qgis2 runtime $HOME/.qgis2/python/plugins
# (symlink on UNIX, copy on Windows)
$ paver install
#
```
