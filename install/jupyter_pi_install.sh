#!/bin/bash

# apt-get installs
sudo apt-get -y update
sudo apt-get -y install build-essential python-dev python-distlib python-setuptools python-pip python-wheel libzmq-dev libgdal-dev
sudo apt-get -y install xsel xclip libxml2-dev libxslt-dev python-lxml python-h5py python-numexpr python-dateutil python-six python-tz python-bs4 python-html5lib python-openpyxl python-tables python-xlrd python-xlwt cython python-sqlalchemy python-xlsxwriter python-jinja2 python-boto python-gflags python-googleapi python-httplib2 python-zmq libspatialindex-dev
sudo apt-get -y install python-requests python-pil python-scrapy python-geopy python-shapely python-pyproj python-scipy

# pip installs
yes | sudo pip install -U pip
yes | sudo pip install bottleneck rtree
yes | sudo pip install jupyter
yes | sudo pip install backports_abc jsonschema singledispatch ipykernel

# run with 'jupyter notebook'

