from trains import TrainApi
from tkinter import *
from trainBoard import TrainBoard
import threading
import time
from datetime import datetime
import json
import ast
import os
import argparse

def loadConfig():
    with open(os.path.dirname(__file__)+'/../config.json', 'r') as programConfig:
        config = json.load(programConfig)
        return config

def updateClock():
    timeVar.set(datetime.now().strftime("%H:%M:%S"))
    root.after(500, updateClock)
 
def updateBoards():
    print("updated")
    if args.test:
        with open("../data/test_data.json", "r") as json_file:
            station_data = json.load(json_file)
    else:
        station_data = trainApi.getStationArrivalsDepartures(station)['trainServices']
    board1.setData(returnServicesForPlatform(station_data, '1'))
    board2.setData(returnServicesForPlatform(station_data, '2'))
    root.after(15000, updateBoards)

def switchOverlays():
    board1.switchOverlay()
    board2.switchOverlay()
    root.after(3000, switchOverlays)

def returnServicesForPlatform(stationServices, platform):
    return [service for service in stationServices if service.get("platform", "") == str(platform)]

def scrollText():
    board1.incrementTextScroll(1)
    board2.incrementTextScroll(1)
    root.after(250, scrollText)

config = loadConfig()
station = config['stationCode']

parser = argparse.ArgumentParser()
parser.add_argument('-t','--test', action="store_true")
args = parser.parse_args()

root=Tk()
root.configure(background='black', cursor='none')
root.geometry('800x480')
root.attributes('-type', 'dock')
platform1 = Label(root, text=' 1 ', fg='black', bg='white', font=('Times New Roman', 30, 'bold'))
platform1.pack(anchor=W, pady=(0,15))
screen = Frame(root, background='black')
screen.grid_propagate(1)
screen.pack(fill=BOTH, expand=1)

platform2 = Label(root, text=' 2 ', fg='black', bg='white', font=('Times New Roman', 30, 'bold'))
platform2.pack(anchor=E, pady=(0,15))
screen2 = Frame(root, background='black')
screen2.grid_propagate(1)
screen2.pack(fill=BOTH, expand=1)
board1 = TrainBoard(screen)
board2 = TrainBoard(screen2)
root.after(15000, updateBoards)
root.after(3000, switchOverlays)
root.after(250, scrollText)

timeVar = StringVar(root)
timeText = Label(root, textvariable=timeVar, fg='orange', bg='black', font=('London Underground', 30))
timeText.pack(fill=BOTH, expand=1)
timeText.after(500, updateClock)

trainApi = TrainApi(config['api_token'])
if args.test:
    with open("../data/test_data.json", "r") as json_file:
        station_data = json.load(json_file)
else:
    station_data = trainApi.getStationArrivalsDepartures(station).get('trainServices', []) 

trainApi = TrainApi(config['api_token'])
board1.setData(returnServicesForPlatform(station_data, '1'))
board2.setData(returnServicesForPlatform(station_data, '2'))
root.mainloop()
