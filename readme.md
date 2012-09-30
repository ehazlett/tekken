# Tekken

Tekken is an admin application for the [Sensu](https://github.com/sensu) monitoring suite.

# Setup

Tekken requires MongoDB and Redis.  The default configuration assumes MongoDB is running on localhost:27017 and Redis is running on localhost:6379.

* `pip install -r requirements.txt`
* `./test_unit.sh`
* `python application.py`
* open browser to (or curl) http://localhost:5000/
