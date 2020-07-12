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

        self.rowA2text = StringVar(root)
        self.rowA3text = StringVar(root)
        self.rowA4text = StringVar(root)

        self.rowB1text = StringVar(root)
        self.rowB2text = StringVar(root)

        self.rowC2text = StringVar(root)
        self.rowC3text = StringVar(root)
        self.rowC4text = StringVar(root)

        self.rowD2text = StringVar(root)
        self.rowD3text = StringVar(root)
        self.rowD4text = StringVar(root)

        self.boardVars = [self.rowA2text, self.rowA3text, self.rowA4text, self.rowC2text, self.rowC3text, self.rowC4text, self.rowD2text, self.rowD3text, self.rowD4text]

        self.overlayRows = [rowC, rowD]

        boardFont='Dot Matrix'
        boardFontSize=30

        self.rowB2text = ""
        self.leadingScroll = -7
        self.scrollPosition = self.leadingScroll
        self.trailingSroll = 10

        rowA1 = Label(rowA, text='1st', width=3, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowA1.pack(side=LEFT, padx=(0,20))

        rowA2 = Label(rowA, textvariable=self.rowA2text, width=5, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowA2.pack(side=LEFT, padx=(0,20))

        rowA3 = Label(rowA, textvariable=self.rowA3text, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowA3.pack(side=LEFT)

        rowA4 = Label(rowA, textvariable=self.rowA4text, fg='orange', bg='black', anchor='e', font=(boardFont, boardFontSize))
        rowA4.pack(side=RIGHT)

        rowB1 = Label(rowB, textvariable=self.rowB1text, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowB1.pack(side=LEFT, padx=(0,20))

        self.rowB2 = Text(rowB, wrap=NONE, height=1, fg='orange', bg='black', bd=-1, font=(boardFont, boardFontSize))

        self.rowB2.pack(side=LEFT)

        rowC1 = Label(rowC, text='2nd', width=3, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowC1.pack(side=LEFT, padx=(0,20))

        rowC2 = Label(rowC, textvariable=self.rowC2text, width=5, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowC2.pack(side=LEFT, padx=(0,20))

        rowC3 = Label(rowC, textvariable=self.rowC3text, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowC3.pack(side=LEFT)

        rowC4 = Label(rowC, textvariable=self.rowC4text, fg='orange', bg='black', anchor='e', font=(boardFont, boardFontSize))
        rowC4.pack(side=RIGHT)

        rowD1 = Label(rowD, text='3rd', width=3, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowD1.pack(side=LEFT, padx=(0,20))

        rowD2 = Label(rowD, textvariable=self.rowD2text, width=5, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowD2.pack(side=LEFT, padx=(0,20))

        rowD3 = Label(rowD, textvariable=self.rowD3text, fg='orange', bg='black', anchor='w', font=(boardFont, boardFontSize))
        rowD3.pack(side=LEFT)

        rowD4 = Label(rowD, textvariable=self.rowD4text, fg='orange', bg='black', anchor='e', font=(boardFont, boardFontSize))
        rowD4.pack(side=RIGHT)


    def clearBoard(self):
        for var in self.boardVars:
            var.set(' ')

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

    def setData(self, services):
        try:
            service = services[0]
            self.rowA2text.set(service['std'])
            self.rowA3text.set(service['destination']['location'][0]['locationName'])
            self.rowA4text.set(service['etd'])

            self.rowB1text.set('Calling at:')
            self.rowB2.delete('1.0', END)
            self.rowB2text = self.generateCallingPointsString(service['subsequentCallingPoints']['callingPointList'][0]['callingPoint'])
            self.rowB2.insert(END, self.rowB2text)
        except IndexError:
            self.rowA2text.set('NO SERVICE')
            self.rowA3text.set('')
            self.rowA4text.set('')

        try:
            service = services[1]
            self.rowC2text.set(service['std'])
            self.rowC3text.set(service['destination']['location'][0]['locationName'])
            self.rowC4text.set(service['etd'])
        except IndexError:
            self.rowC2text.set('NO SERVICE')
            self.rowC3text.set('')
            self.rowC4text.set('')

        try:
            service = services[2]
            self.rowD2text.set(service['std'])
            self.rowD3text.set(service['destination']['location'][0]['locationName'])
            self.rowD4text.set(service['etd'])
        except IndexError:
            self.rowD2text.set('NO SERVICE')
            self.rowD3text.set('')
            self.rowD4text.set('')
