from trains import TrainApi
from tkinter import *
from trainBoard import TrainBoard
import threading
import time
from datetime import datetime
import json
import ast

def updateClock(label, refreshTime):
    while True:
        label.set(datetime.now().strftime("%H:%M:%S"))
        time.sleep(refreshTime)

def updateBoards():
    board1.setData(trainApi.getStationArrivalsDepartures('<station>')['service'])
    print('updated screen...')
    print(datetime.now())
    root.after(15000, updateBoards)

def switchOverlays():
    board1.switchOverlay()
    root.after(3000, switchOverlays)

def scrollText():
    board1.incrementTextScroll(1)
    root.after(250, scrollText)

root=Tk()
root.geometry('800x480')
screen = Frame(root, background='black')
screen.grid_propagate(1)
screen.pack(fill=BOTH, expand=1)
board1 = TrainBoard(screen)
root.after(150000, updateBoards)
root.after(3000, switchOverlays)
root.after(250, scrollText)

timeVar = StringVar(root)
timeText = Label(root, textvariable=timeVar, fg='orange', bg='black', font=('Dot Matrix', 50))
timeText.pack(fill=BOTH, expand=1)
timeThread = threading.Thread(target=updateClock, args=(timeVar,0.5,))
timeThread.start()

with open('../data/testData.txt') as data_file:
    test_data=ast.literal_eval(data_file.read())

trainApi = TrainApi("<token>")
#board1.setData(trainApi.getStationArrivalsDepartures('<station>')['service'])
board1.setData(test_data)
root.mainloop()
