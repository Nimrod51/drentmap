from __future__ import print_function
import os
import json
import time
from .data import DATADIR


class Scraper():
    """
    An interface, that each web scraper implements
    """

    def __init__(self, location=None, name="ScraperAPI"):
        self.name = name
        self.location = location
        self.sleepTime = 5
        self.gendir()

    def setLocation(self, location):
        self.location = location

    # wait for a while, so Scraper doesn't poll websites too often
    def sleep(self, t=-1):
        if t == -1:
            t = self.sleepTime
        time.sleep(t)

    def gendir(self):
        self.datadir = os.path.join(DATADIR, self.name)
        if not os.path.exists(self.datadir):
            os.mkdir(self.datadir)
        if not os.path.exists(os.path.join(self.datadir, "raw/")):
            os.mkdir(os.path.join(self.datadir, "raw/"))

    # get date of last check of the website
    @property
    def lastChecked(self):
        with open(os.path.join(self.datadir + "lastcheck.ini")) as f:
            try:
                return int(f.read())
            except Exception:
                return -1

    # check for new datapoints on the website
    def check(self):
        # make sure a data directory is present
        self.gendir()
        # update lastChecked
        with open(os.path.join(self.datadir + "lastcheck.ini"), "w+") as f:
            print(int(time.time()), file=f)

    # formatted status of scraping
    def printStatus(self, i, outof=-1):
        if outof == -1:
            print(i, "flats.")
        print(i, "/", outof, "flats.")

    # output of a dict of data in JSON format to a file named after id
    def output(self, dict, id):
        with open(os.path.join(self.datadir, str(id)+".json"), "w+") as outf:
            outf.write(json.dumps(dict))
