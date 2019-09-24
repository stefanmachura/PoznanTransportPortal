import requests
import unittest
import json
import os
import time
import sys
from datetime import datetime
from pathlib import Path

SUFFIX = "_JSON.txt"
DATADIR = os.path.join(sys.path[0], Path("PoznanUtilitiesData/"))
LOGFILENAME = os.path.join(DATADIR, "log.txt")


def log_event(txt):
    logstring = " ".join((datetime.utcnow().strftime('%d.%m.%y - %H:%M:%S.%f'), txt, "\n"))

    if os.path.isfile(LOGFILENAME):
        with open(LOGFILENAME, "a") as logfile:
            logfile.write(logstring)
    else:
        with open(LOGFILENAME, "w") as logfile:
            logfile.write(logstring)


class UtilitiesAPIHandling:
    def __init__(self, desc, url):
        if not os.path.exists(DATADIR):
            os.mkdir(DATADIR)
        self.filename = os.path.join(DATADIR, desc + SUFFIX)
        self.desc = desc
        self.url = url
        self.status_code = 0
        self.service_api_json = ""
        self.load_json_from_either_api_or_file()

    def get_file_age(self):
        if os.path.isfile(self.filename):
            return int(time.time() - os.path.getmtime(self.filename))
        else:
            return -1

    def get_json(self):
        return self.service_api_json

    def save_json_to_file(self):
        with open(self.filename, "w") as jsonfile:
            json.dump(self.get_json(), jsonfile)
        log_event(self.desc + " was saved to file")

    def read_json_from_file(self):
        with open(self.filename, "r") as jsonfile:
            self.service_api_json = json.load(jsonfile)
        log_event(self.desc + " was read from file")

    def download_json_from_api(self):
        try:
            r = requests.get(self.url)
            r.encoding = "utf-8"
            self.status_code = r.status_code
        except ConnectionError:
            return {}
        self.status_code = r.status_code
        self.service_api_json = r.json()
        log_event(self.desc + " was read from online API")

    def load_json_from_either_api_or_file(self, max_age=30):
        log_event(self.desc + " request logged, the file is " + str(self.get_file_age()) + " seconds old")
        if self.get_file_age() in range(0, max_age):
            self.read_json_from_file()
        else:
            self.download_json_from_api()
            self.save_json_to_file()
