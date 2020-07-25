from tkinter import *
import time

class ServiceRow:

    def __init__(self, root, position):
        boardFont='Dot Matrix'
        boardFontSize=30

        root = root

        self.departureTimeText = StringVar(root)
        self.destinationText = StringVar(root)
        self.statusText = StringVar(root)

        position = Label(root, text=position, width=3, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        position.pack(side=LEFT, padx=(0,20))

        self.departureTime = Label(root, textvariable=self.departureTimeText, width=5, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        self.departureTime.pack(side=LEFT, padx=(0,20))

        self.destination = Label(root, textvariable=self.destinationText, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        self.destination.pack(side=LEFT)

        self.status = Label(root, textvariable=self.statusText, fg='orange', bg='black', anchor='e', font=(boardFont, boardFontSize))
        self.status.pack(side=RIGHT)

    def update(self, departureTime, destination, status):
        self.departureTime.config(width=5)
        self.departureTimeText.set(departureTime)
        self.destinationText.set(destination)
        self.statusText.set(status)

    def setNoService(self):
        self.departureTime.config(width=10)
        self.departureTimeText.set('NO SERVICE')
        self.destinationText.set('')
        self.statusText.set('')


class TrainBoard:

    def __init__(self, root):
        self.root = root
        self.rowA = Frame(root, bg='black', width=1300)
        self.rowB = Frame(root, bg='black', width=1300)
        self.rowC = Frame(root, bg='black', width=1300)
        self.rowD = Frame(root, bg='black', width=1300)

        root.grid_columnconfigure(0, weight=1)

        self.rowA.grid(row=0, column=0, sticky="we")
        self.rowB.grid(row=1, column=0, sticky="we")
        self.rowD.grid(row=2, column=0, sticky="we")
        self.rowC.grid(row=2, column=0, sticky="we")

        self.service1st = ServiceRow(self.rowA, '1st')
        self.service2nd = ServiceRow(self.rowC, '2nd')
        self.service3rd = ServiceRow(self.rowD, '3rd')

        self.rowB1text = StringVar(root)
        self.rowB2text = StringVar(root)

        self.overlayRows = [self.rowC, self.rowD]

        self.currentServices = []

        boardFont='Dot Matrix'
        boardFontSize=30

        self.rowB2text = ""
        self.leadingScroll = -7
        self.scrollPosition = self.leadingScroll
        self.trailingSroll = 10

        rowB1 = Label(self.rowB, textvariable=self.rowB1text, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowB1.pack(side=LEFT, padx=(0,20))

        self.rowB2 = Text(self.rowB, wrap=NONE, height=1, fg='orange', bg='black', bd=-1, font=(boardFont, boardFontSize))
        self.rowB2.pack(side=LEFT)

    def switchOverlay(self):
        self.overlayRows.reverse()
        self.overlayRows[0].tkraise()

    def generateCallingPointsString(self, callingPoints):
        callingPointsNames = [ callingPoint['locationName'] for callingPoint in callingPoints ]
        return ', '.join(callingPointsNames[:-1]) + ' and ' + callingPointsNames[-1] + '.'

    def incrementTextScroll(self, number):
        if self.scrollPosition <= 0:
            self.scrollPosition += number
            return
        elif self.scrollPosition == len(self.rowB2text):
            self.scrollPosition = self.leadingScroll
#            self.rowB2.xview_moveto(1)
            self.rowB2.xview_scroll(-len(self.rowB2text)-1, UNITS)
            return
        else:
            self.scrollPosition += number
            self.rowB2.xview(MOVETO, self.scrollPosition/len(self.rowB2text))

    def hideRows(self):
        self.rowA.grid_remove()
        self.rowB.grid_remove()
        self.rowC.grid_remove()
        self.rowD.grid_remove()

    def showRows(self):
        self.rowA.grid()
        self.rowB.grid()
        self.rowC.grid()
        self.rowD.grid()

    def extractDataFromService(self, service):
        departureTime = service['std']
        destination = service['destination']['location'][0]['locationName']
        status = service['etd']
        return departureTime, destination, status

    def setData(self, services):
        '''
        A wrapper around setData2 so that we can hide data and create a callback to setData2 
        in the event of a change to service, simulating a momentary blank screen without halting
        the rest of the program.
        '''

        # If services is [] (no services) and currentServices is [], it could be that the app
        # has just started up and its late at night (so no further services). We still want
        # want to set data in this scenario to display NO SERVICE.
        if services == [] and self.currentServices == []:
            self.setData2(services)
            return
        elif services[:3] == self.currentServices:
            return
        else:
            self.hideRows()
            self.root.after(500, self.setData2, services)

    def setData2(self, services):

        try:
            service = services[0]
            departureTime, destination, status = self.extractDataFromService(service)
            self.service1st.update(departureTime, destination, status)

            self.rowB1text.set('Calling at:')
            self.rowB2.delete('1.0', END)
            self.rowB2text = self.generateCallingPointsString(service['subsequentCallingPoints']['callingPointList'][0]['callingPoint'])
            self.rowB2.insert(END, self.rowB2text)
        except IndexError:
            self.service1st.setNoService()

        try:
            service = services[1]
            departureTime, destination, status = self.extractDataFromService(service)
            self.service2nd.update(departureTime, destination, status)
        except IndexError:
            self.service2nd.setNoService()

        try:
            service = services[2]
            departureTime, destination, status = self.extractDataFromService(service)
            self.service3rd.update(departureTime, destination, status)
        except IndexError:
            self.service3rd.setNoService()

        self.currentServices = services[:3]
        self.showRows()
