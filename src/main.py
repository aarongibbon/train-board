from trains import TrainApi
from tkinter import *
from trainBoard import TrainBoard
import threading
import time
from datetime import datetime
import json
import ast

def loadConfig():
    with open('../config.json', 'r') as programConfig:
        config = json.load(programConfig)
        return config

def updateClock():
    timeVar.set(datetime.now().strftime("%H:%M:%S"))
    root.after(500, updateClock)
 
def updateBoards():
    stationData = trainApi.getStationArrivalsDepartures(station)['service']
    board1.setData(returnServicesForPlatform(stationData, '1'))
    board2.setData(returnServicesForPlatform(stationData, '2'))
    print('updated screen...')
    print(datetime.now())
    root.after(15000, updateBoards)

def switchOverlays():
    board1.switchOverlay()
    board2.switchOverlay()
    root.after(3000, switchOverlays)

def returnServicesForPlatform(stationServices, platform):
    return [service for service in stationServices if service['platform'] == str(platform)]

def scrollText():
    board1.incrementTextScroll(1)
    board2.incrementTextScroll(1)
    root.after(250, scrollText)

config = loadConfig()

station = config['stationCode']

root=Tk()
root.configure(background='black', cursor='none')
root.geometry('800x480')
root.attributes('-type', 'dock')
platform1 = Label(root, text=' 1 ', fg='black', bg='white', font=('Times New Roman', 30, 'bold'))
platform1.pack(anchor=W)
screen = Frame(root, background='black')
screen.grid_propagate(1)
screen.pack(fill=BOTH, expand=1)

platform2 = Label(root, text=' 2 ', fg='black', bg='white', font=('Times New Roman', 30, 'bold'))
platform2.pack(anchor=E)
screen2 = Frame(root, background='black')
screen2.grid_propagate(1)
screen2.pack(fill=BOTH, expand=1)
board1 = TrainBoard(screen)
board2 = TrainBoard(screen2)
root.after(15000, updateBoards)
root.after(3000, switchOverlays)
root.after(250, scrollText)

timeVar = StringVar(root)
timeText = Label(root, textvariable=timeVar, fg='orange', bg='black', font=('Dot Matrix', 30))
timeText.pack(fill=BOTH, expand=1)
timeText.after(500, updateClock)

#with open('../data/testDataDoubleNoService.txt') as data_file:
#    test_data=ast.literal_eval(data_file.read())

#with open('../data/testData2.txt') as data_file:
#    test_data2=ast.literal_eval(data_file.read())

trainApi = TrainApi(config['apiToken'])
stationData = trainApi.getStationArrivalsDepartures(station)['service']
board1.setData(returnServicesForPlatform(stationData, '1'))
board2.setData(returnServicesForPlatform(stationData, '2'))
root.mainloop()
