import threading
import tkinter as tk
from functools import partial
from tkinter import messagebox
import numpy as np

import Controller as gc


# thread


class GuiInterface:
    event = gc.Event()
    arrButton = {}
    memory = []
    sizeRow = 13
    sizeCol = 13
    checked = np.zeros((sizeRow, sizeCol))

    def setCondition(self, condition):
        self.event.setCondition(condition)

    def setGuiI(self, guiI):
        self.guiI = guiI

    def callInfinite(self):
        self.root.mainloop()

    def drawReset(self, x, y):
        self.reset = tk.Button(self.window, text="reset game", font=('arial', 15, 'bold'), relief="raised", bg='gray',
                               foreground="white",
                               command=partial(self.event.clickedReset, guiI=self.guiI))
        self.reset.place(x=x, y=y)

    def drawUndo(self, x, y):
        self.undo = tk.Button(self.window, text="undo", font=('arial', 15, 'bold'), relief="raised", bg='gray',
                              foreground="white",
                              command=partial(self.event.clickedUndo, guiI=self.guiI)
                              )
        self.undo.place(x=x, y=y)

    def drawBox(self):
        self.root = tk.Tk()
        self.window = tk.Frame(self.root, width=640, height=640, background="bisque")
        self.window.place(x=0, y=0)
        self.window.pack(fill=None, expand=False)
        self.root.title("Welcome to Caro")
        self.root.geometry("640x600")
        self.root.eval('tk::PlaceWindow . center')
        self.root.resizable(0, 0)

    def drawContourLines(self):
        self.place_y = 30
        for x in range(self.sizeRow):
            self.place_x = 30
            for y in range(self.sizeCol):
                self.arrButton[x, y] = tk.Button(self.window, font=('arial', 15, 'bold'), height=1, width=2,
                                                 borderwidth=1, relief="solid", bg='white'
                                                 , command=partial(self.event.clicked, x=x, y=y, guiI=self.guiI)
                                                 )
                self.arrButton[x, y].grid(row=x, column=y)
                self.arrButton[x, y].place(x=self.place_x, y=self.place_y)
                self.place_x += 35
            self.place_y += 42
        self.place_y = 30
        self.place_x = 30

    def drawChessBoard(self):
        self.drawBox()
        self.drawContourLines()
        self.drawReset(self.place_x * (self.sizeCol + 4), self.place_y)
        self.drawUndo(self.place_x * (self.sizeCol + 4), self.place_y + 42)

    def changeColor(self):
        sz = len(self.memory)
        print("size = ", sz)
        if sz > 0:
            x = self.memory[sz - 1][0]
            y = self.memory[sz - 1][1]
            self.arrButton[x, y].configure(bg="green")
            if sz > 1:
                x = self.memory[sz - 2][0]
                y = self.memory[sz - 2][1]
                self.arrButton[x, y].configure(bg="white")

    def isDifferent(self, x, y, id):
        return self.checked[x][y] > 0 and self.checked[x][y] != id

    def getArrButton(self, x, y):
        return self.arrButton[x, y]['text']

    def setArrButton(self, x, y, val):
        self.arrButton[x, y]['text'] = val

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()



    def showTableCaro(self):
        self.drawChessBoard()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
