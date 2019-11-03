#!/bin/sh -l

pip install -r requirements-crawl.txt
python -m crawlers $1
