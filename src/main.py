import argparse
import json
import os
from tkinter import *

from trainBoard import StationBoard


def loadConfig():
    with open(os.path.dirname(__file__) + "/../config.json", "r") as programConfig:
        config = json.load(programConfig)
        return config


config = loadConfig()
station = config["stationCode"]

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", action="store_true")
args = parser.parse_args()

StationBoard(station, config["api_token"], test=args.test)
