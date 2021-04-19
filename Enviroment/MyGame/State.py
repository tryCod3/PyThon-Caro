import Player as pl
import Point as point
import numpy as np


def whoNext(guiI):
    if (len(guiI.memory) % 2 == 0):
        return pl.EntityPlayer.ai
    else:
        return pl.EntityPlayer.user


def isFullBoard(guiI):
    sz = len(guiI.memory)
    return sz == (guiI.sizeRow * guiI.sizeCol)


def inRanger(lx, rx, val):
    return val >= lx and val <= rx


def listCanGo(guiI):
    list = []
    sz = len(guiI.memory)
    checked = np.zeros((guiI.sizeRow, guiI.sizeCol))
    for i in range(sz):
        x = guiI.memory[i][0]
        y = guiI.memory[i][1]
        for q in range(-1, 2):
            for e in range(-1, 2):
                xx = x + q
                yy = y + e
                if isInBoard(xx, yy, guiI) and guiI.checked[xx][yy] == 0 and checked[xx][yy] == 0:
                    list.append(point.Point(xx, yy))
                    checked[xx][yy] = 1
    return list


def isInBoard(x, y, guiI):
    if x >= 0 and x < guiI.sizeRow and y >= 0 and y < guiI.sizeCol:
        return True
    return False


def hasWin(id, guiI):
    sz = len(guiI.memory)
    if sz < 5: return False
    if sz > 0:
        for k in range(sz):
            x = guiI.memory[k][0]
            y = guiI.memory[k][1]
            if guiI.checked[x][y] != id: continue
            # ngangRight
            cntID = 0
            for i in range(y, y + 5):
                if i >= guiI.sizeCol: break
                if guiI.checked[x][i] != id: break
                cntID += 1
            if cntID == 5: return True
            # ngangLeft
            cntID = 0
            for i in range(y - 4, y + 1):
                if i < 0: break
                if guiI.checked[x][i] != id: break
                cntID += 1
            if cntID == 5: return True
            # Up
            cntID = 0
            for i in range(x - 4, x + 1):
                if i < 0: break
                if guiI.checked[i][y] != id: break
                cntID += 1
            if cntID == 5: return True
            # Down
            cntID = 0
            for i in range(x, x + 5):
                if i >= guiI.sizeRow: break
                if guiI.checked[i][y] != id: break
                cntID += 1
            if cntID == 5: return True
            # cheoChinhXuong
            cntID = 0
            i, j = x, y
            time = 5
            while time > 0 and i < guiI.sizeRow and j < guiI.sizeCol:
                if guiI.checked[i][j] != id: break
                cntID += 1
                i += 1
                j += 1
                time -= 1
            if cntID == 5: return True
            # cheoChinhLen
            cntID = 0
            i, j = x, y
            time = 5
            while time > 0 and i >= 0 and j >= 0:
                if guiI.checked[i][j] != id: break
                cntID += 1
                i -= 1
                j -= 1
                time -= 1
            if cntID == 5: return True
            # cheoPhuXuong
            cntID = 0
            i, j = x, y
            time = 5
            while time > 0 and i < guiI.sizeRow and j >= 0:
                if guiI.checked[i][j] != id: break
                cntID += 1
                i += 1
                j -= 1
                time -= 1
            if cntID == 5: return True
            # cheoPhuLen
            cntID = 0
            i, j = x, y
            time = 5
            while time > 0 and i >= 0 and j < guiI.sizeCol:
                if guiI.checked[i][j] != id: break
                cntID += 1
                i -= 1
                j += 1
                time -= 1
            if cntID == 5: return True
    return False
