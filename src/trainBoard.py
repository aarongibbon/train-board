from tkinter import *

class TrainBoard:

    def __init__(self, root):

        rowA = Frame(root, bg='black', width=1300)
        rowB = Frame(root, bg='black', width=1300)
        rowC = Frame(root, bg='black', width=1300)
        rowD = Frame(root, bg='black', width=1300)

        root.grid_columnconfigure(0, weight=1)

        rowA.grid(row=0, column=0, sticky="we")
        rowB.grid(row=1, column=0, sticky="we")
        rowD.grid(row=2, column=0, sticky="we")
        rowC.grid(row=2, column=0, sticky="we")

        self.rowA1text = StringVar(root)
        self.rowA2text = StringVar(root)
        self.rowA3text = StringVar(root)

        self.rowB1text = StringVar(root)
        self.rowB2text = StringVar(root)

        self.rowC1text = StringVar(root)
        self.rowC2text = StringVar(root)
        self.rowC3text = StringVar(root)

        self.rowD1text = StringVar(root)
        self.rowD2text = StringVar(root)
        self.rowD3text = StringVar(root)

        self.boardVars = [self.rowA1text, self.rowA2text, self.rowA3text, self.rowC1text, self.rowC2text, self.rowC3text, self.rowD1text, self.rowD2text, self.rowD3text]

        self.overlayRows = [rowC, rowD]

        boardFont='Dot Matrix'
        boardFontSize=50

        rowA1 = Label(rowA, textvariable=self.rowA1text, width=5, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowA1.pack(side=LEFT, padx=(0,20))

        rowA2 = Label(rowA, textvariable=self.rowA2text, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowA2.pack(side=LEFT)

        rowA3 = Label(rowA, textvariable=self.rowA3text, fg='orange', bg='black', anchor='e', font=(boardFont, boardFontSize))
        rowA3.pack(side=RIGHT)

        rowB1 = Label(rowB, textvariable=self.rowB1text, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowB1.pack(side=LEFT, padx=(0,20))

        self.rowB2 = Text(rowB, wrap=NONE, height=1, fg='orange', bg='black', bd=-1, font=(boardFont, boardFontSize))

        self.rowB2.pack(side=LEFT)

        rowC1 = Label(rowC, textvariable=self.rowC1text, width=5, fg='orange', bg='red', anchor='w', font=(boardFont, boardFontSize))
        rowC1.pack(side=LEFT, padx=(0,20))

        rowC2 = Label(rowC, textvariable=self.rowC2text, fg='orange', bg='blue', anchor='w', font=(boardFont, boardFontSize))
        rowC2.pack(side=LEFT)

        rowC3 = Label(rowC, textvariable=self.rowC3text, fg='orange', bg='green', anchor='e', font=(boardFont, boardFontSize))
        rowC3.pack(side=RIGHT)

        rowD1 = Label(rowD, textvariable=self.rowD1text, width=5, fg='orange', bg='red', anchor='w', font=(boardFont, boardFontSize))
        rowD1.pack(side=LEFT, padx=(0,20))

        rowD2 = Label(rowD, textvariable=self.rowD2text, fg='orange', bg='blue', anchor='w', font=(boardFont, boardFontSize))
        rowD2.pack(side=LEFT)

        rowD3 = Label(rowD, textvariable=self.rowD3text, fg='orange', bg='green', anchor='e', font=(boardFont, boardFontSize))
        rowD3.pack(side=RIGHT)


    def clearBoard(self):
        for var in self.boardVars:
            var.set(' ')

    def switchOverlay(self):
        self.overlayRows.reverse()
        self.overlayRows[0].tkraise()

    def generateCallingPointsString(self, callingPoints):
        callingPointsNames = [ callingPoint['locationName'] for callingPoint in callingPoints ]
        return ', '.join(callingPointsNames)

    def setData(self, services):
        try:
            service = services[0]
            self.rowA1text.set(service['std'])
            self.rowA2text.set(service['destination']['location'][0]['locationName'])
            self.rowA3text.set(service['etd'])

            self.rowB1text.set('Calling at:')
            self.rowB2.delete('1.0', END)
            self.rowB2.insert(END, self.generateCallingPointsString(service['subsequentCallingPoints']['callingPointList'][0]['callingPoint']))
        except IndexError:
            self.rowA1text.set('NO SERVICE')
            self.rowA2text.set('')
            self.rowA3text.set('')

        try:
            service = services[1]
            self.rowC1text.set(service['std'])
            self.rowC2text.set(service['destination']['location'][0]['locationName'])
            self.rowC3text.set(service['etd'])
        except IndexError:
            self.rowC1text.set('NO SERVICE')
            self.rowC2text.set('')
            self.rowC3text.set('')

        try:
            service = services[2]
            self.rowD1text.set(service['std'])
            self.rowD2text.set(service['destination']['location'][0]['locationName'])
            self.rowD3text.set(service['etd'])
        except IndexError:
            self.rowD1text.set('NO SERVICE')
            self.rowD2text.set('')
            self.rowD3text.set('')
