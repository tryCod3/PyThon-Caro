import threading
from tkinter import messagebox

import Player as pl
import State as st
import numpy as np


class Event(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def setCondition(self, condition):
        self.condition = condition

    def notification(self, title, msg):
        messagebox.showinfo(str(title), str(msg))

    def clicked(self, x, y, guiI):
        if st.isFullBoard(guiI) == False and pl.EntityPlayer.win == pl.EntityPlayer.noOneHasLost and st.whoNext(
                guiI) == pl.EntityPlayer.user:
            if guiI.getArrButton(x, y) == "":
                guiI.setArrButton(x, y, 'X')
                guiI.memory.append([x, y])
                guiI.changeColor()
                guiI.checked[x][y] = 2
                if st.hasWin(pl.EntityPlayer.user, guiI):
                    pl.EntityPlayer.win = True
                    self.notification("Winner for ", 'X')
                print("next Ai")
                self.condition.set()

    def clickedUndo(self, guiI):
        if self.condition.isSet() == False and len(
                guiI.memory) - 2 >= 0 and pl.EntityPlayer.win == pl.EntityPlayer.noOneHasLost:
            sz = len(guiI.memory)
            if sz > 2:
                self.off(guiI)
                self.off(guiI)
                self.light(guiI)
            elif sz == 2:
                self.off(guiI)
                self.light(guiI)


    def clickedReset(self, guiI):
        if self.condition.isSet() == False:
            while len(guiI.memory) > 0:
                self.off(guiI)
            self.setAiWin()
            self.resetAi()
            guiI.checked = np.zeros((guiI.sizeRow, guiI.sizeCol))

    def off(self, guiI):
        sz = len(guiI.memory)
        x = guiI.memory[sz - 1][0]
        y = guiI.memory[sz - 1][1]
        guiI.checked[x][y] = 0
        guiI.setArrButton(x, y, "")
        guiI.arrButton[x, y].configure(bg="white")
        guiI.memory.pop()

    def light(self, guiI):
        sz = len(guiI.memory)
        x = guiI.memory[sz - 1][0]
        y = guiI.memory[sz - 1][1]
        guiI.arrButton[x, y].configure(bg="green")

    def setAiWin(self):
        self.condition.set()
        pl.EntityPlayer.win = True

    def resetAi(self):
        self.condition.clear()
        pl.EntityPlayer.win = False
