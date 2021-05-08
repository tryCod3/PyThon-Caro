import threading
import time
from tkinter import messagebox

import Player as pl
import State as st
import numpy as np
import Ai as ai


class Event(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def setCondition(self, condition):
        self.condition = condition

    def setCondition_Choise(self, condition_choise):
        self.condition_choise = condition_choise

    def notification(self, title, msg):
        messagebox.showinfo(str(title), str(msg))

    def clicked(self, x, y, guiI):
        if pl.EntityPlayer.user == pl.EntityPlayer.realNext and pl.EntityPlayer.win == pl.EntityPlayer.noOneHasLost:
            if guiI.getArrButton(x, y) == "":
                guiI.setArrButton(x, y, 'X')
                guiI.memory.append([x, y])
                guiI.changeColor()
                guiI.checked[x][y] = 2
                pl.EntityPlayer.realNext = pl.EntityPlayer.ai
                if st.hasWin(pl.EntityPlayer.user, guiI):
                    pl.EntityPlayer.win = True
                    self.notification("Winner for ", 'X')
                print("next Ai")
                self.condition.set()

    def AivsAi(self, guiI):
        self.clickedReset(guiI)
        pl.EntityPlayer.vsUser = False
        self.condition_choise.set()

    def AivsUser(self, guiI):
        self.clickedReset(guiI)
        pl.EntityPlayer.vsUser = True
        self.condition_choise.set()

    def clickedUndo(self, guiI):
        if pl.EntityPlayer.user == pl.EntityPlayer.realNext and pl.EntityPlayer.win == pl.EntityPlayer.noOneHasLost:
            sz = len(guiI.memory)
            if sz > 2:
                self.off(guiI)
                self.off(guiI)
                self.light(guiI)
            elif sz == 2:
                self.off(guiI)
                self.light(guiI)

    def clickedReset(self, guiI):
        if pl.EntityPlayer.user == pl.EntityPlayer.realNext:
            while len(guiI.memory) > 0:
                self.off(guiI)
            self.setAiWin()
            time.sleep(0.5)
            self.resetAi()
            guiI.checked = np.zeros((guiI.sizeRow, guiI.sizeCol))
            pl.EntityPlayer.win = False
            pl.EntityPlayer.realNext = pl.EntityPlayer.ai
            pl.EntityPlayer.vsUser = None

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
