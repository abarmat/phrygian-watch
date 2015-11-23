# phrygian-watch

## Goal

The aim of phrygian-watch is to digitally oversee the election process of democracies around the world.

## Requirements
* Scrapy: http://scrapy.org/
* grequests: https://github.com/kennethreitz/grequests
* pymongo: https://api.mongodb.org/python/current/

## Install
`pip install -r requirements.txt`

Please refer to specific library requirements and dependencies.

## Run
Run `scrapy list` to list available scrappers.

**Steps**

1) Run a specific spider
`scrapy crawl ean2015`

2) Import the file with the details about documents into mongodb
`mongoimport --db ean2015 --collection docs dump.json`

3) Download the actual docs in pdf format with the downloader located within the extras folder `python downloader.py`. This script will place a /data folder where it's run with the files named according to the format defined by the site.

