import numpy as np

import Point as point
from Enviroment.MyGame import Gui
import Player as pl

arrAttack = [
    [0, 0],
    [1, 1],
    [100, 30],
    [1000, 300],
    [100000, 30000],
    [10000000, 10000000]
]

arrDefen = [0, 100, 1000, 15000, 100000, 150000]


class Experience:

    def think(self, id, guiI):
        sum = 0
        sz = len(guiI.memory)
        if sz > 0:
            for i in range(sz):
                x = guiI.memory[i][0]
                y = guiI.memory[i][1]
                if guiI.checked[x][y] == id:
                    newPoint = point.Point(x, y)
                    sum += self.attack(newPoint, id, guiI)

            sz = len(guiI.memory)
            x = guiI.memory[sz - 1][0]
            y = guiI.memory[sz - 1][1]
            if guiI.checked[x][y] == id:
                if id == pl.EntityPlayer.ai:
                    id = pl.EntityPlayer.user
                else:
                    id = pl.EntityPlayer.ai
                sumDefen = self.defen(point.Point(x, y), id, guiI)
                sum += sumDefen

        return sum

    def setUpArrDefen(self, list):
        w = np.array([0, 0, 0, 0, 0, 0], dtype=int)
        for i in range(len(list)):
            if list[i] == 0:
                continue
            else:
                w[list[i]] = w[list[i]] + 1
        return w

    def defen(self, newPoint, id, guiI):
        defen = self.getDefen(newPoint, id, guiI)

        for i in range(len(defen)):
            if defen[i] > 5:
                defen[i] = 5

        w = self.setUpArrDefen(defen)

        i = 4
        while i >= 1:
            j = i
            while j >= 1:
                if i == j:
                    if w[i] >= 2:
                        w[i + 1] += 1
                        w[i] = 0
                else:
                    if w[i] >= 1 and w[j] >= 1:  # i > j
                        w[i + 1] += 1
                        w[i] = 0
                        w[j + 1] += 1
                        w[j] = 0
                j -= 1
            i -= 1
        sumAtPoint = 0
        for i in range(1 , 6):
            if w[i] > 0:
                sumAtPoint += arrDefen[i]
        return sumAtPoint

    def getDefen(self, point, id, guiI):
        x = point.x
        y = point.y

        # ngang
        i, j = x, y
        diff_ngang = 0
        time = 4
        while time > 0 and j >= 0:
            if guiI.isDifferent(x, j , id):
                diff_ngang += 1
            if j - 1 < 0 or guiI.checked[x][j] == id:
                break
            j -= 1
            time -= 1

        time = 4
        i, j = x, y
        while time > 0 and j < guiI.sizeCol:
            if guiI.isDifferent(x, j , id):
                diff_ngang += 1
            if j + 1 >= guiI.sizeCol or guiI.checked[x][j] == id:
                break
            j += 1
            time -= 1

        # doc
        i, j = x, y
        diff_doc = 0
        time = 4
        while time > 0 and i >= 0:
            if guiI.isDifferent(i, y, id) :
                diff_doc += 1
            if i - 1 < 0 or guiI.checked[i][y] == id :
                break
            i -= 1
            time -= 1

        i, j = x, y
        time = 4
        while time > 0 and i < guiI.sizeRow:
            if guiI.isDifferent(i, y, id):
                diff_doc += 1
            if i + 1 >= guiI.sizeRow or  guiI.checked[i][y] == id :
                break
            i += 1
            time -= 1

        # dcc
        i, j = x, y
        diff_dcc = 0
        time = 4
        while time > 0 and i >= 0 and j >= 0:
            if  guiI.isDifferent(i, j, id):
                diff_dcc += 1
            if i - 1 < 0 or j - 1 < 0 or guiI.checked[i][j] == id:
                break
            i -= 1
            j -= 1
            time -= 1

        i, j = x, y
        time = 4
        while time > 0 and i < guiI.sizeRow and j < guiI.sizeCol:
            if guiI.isDifferent(i, j, id):
                diff_dcc += 1
            if i + 1 >= guiI.sizeRow or j + 1 >= guiI.sizeCol or guiI.checked[i][j] == id :
                break
            i += 1
            j += 1
            time -= 1

        # dcp
        i, j = x, y
        diff_dcp = 0
        time = 4
        while time > 0 and i >= 0 and j < guiI.sizeCol:
            if guiI.isDifferent(i, j, id) :
                diff_dcp += 1
            if i - 1 < 0 or j + 1 >= guiI.sizeCol or  guiI.checked[i][j] == id:
                break
            i -= 1
            j += 1
            time -= 1

        i, j = x, y
        time = 4
        while time > 0 and i < guiI.sizeRow and j >= 0:
            if guiI.isDifferent(i, j, id) :
                diff_dcp += 1
            if i + 1 >= guiI.sizeRow or j - 1 < 0 or guiI.checked[i][j] == id:
                break
            i += 1
            j -= 1
            time -= 1

        list = np.array(
            [ diff_ngang , diff_doc , diff_dcp , diff_dcc ],
            dtype=int)


        return list

    def attack(self, point, id, guiI):
        listHorizal = self.getHorizal(point, id, guiI)
        listVertical = self.getVertical(point, id, guiI)
        listDiagonalMain = self.getDiagonalMain(point, id, guiI)
        listDiagonalSecond = self.getDiagonalSecond(point, id, guiI)
        sum = 0

        listAll = []
        # print("ngang")
        for i in range(len(listHorizal)):
            # print(listHorizal[i].get_x(), " ", listHorizal[i].get_y())
            listAll.append([listHorizal[i].get_x(), listHorizal[i].get_y()])
        # print("doc")
        for i in range(len(listVertical)):
            # print(listVertical[i].get_x(), " ", listVertical[i].get_y())
            listAll.append([listVertical[i].get_x(), listVertical[i].get_y()])
        # print("dcc")
        for i in range(len(listDiagonalMain)):
            # print(listDiagonalMain[i].get_x(), " ", listDiagonalMain[i].get_y())
            listAll.append([listDiagonalMain[i].get_x(), listDiagonalMain[i].get_y()])
        # print("dcp")
        for i in range(len(listDiagonalSecond)):
            # print(listDiagonalSecond[i].get_x(), " ", listDiagonalSecond[i].get_y())
            listAll.append([listDiagonalSecond[i].get_x(), listDiagonalSecond[i].get_y()])

        for i in range(len(listAll)):
            xx = listAll[i][0]
            yy = listAll[i][1]
            sum += arrAttack[xx][yy]

        return sum

    def getHorizal(self, point, id, guiI):
        list = []
        x = point.get_x()
        y = point.get_y()
        bg = max(0, y - 4)
        i = y
        while i >= bg:
            if guiI.isDifferent(x, i, id):
                bg = i + 1
                break
            if i - 1 < bg: break;
            i -= 1

        en = min(guiI.sizeCol - 1, y + 4)
        i = y
        while i <= en:
            if guiI.isDifferent(x, i, id):
                en = i - 1
                break
            if i + 1 > en:  break
            i += 1
        if en - bg + 1 >= 5:
            for i in range(bg, y + 1):
                mx = 0
                self.setup()
                en2 = min(i + 4, guiI.sizeCol - 1)
                for k in range(i, en2 + 1):
                    if guiI.isDifferent(x, k, id):
                        en2 = k - 1
                        break
                if en2 > en: break
                for j in range(i, en2 + 1):
                    if guiI.checked[x][j] == id:
                        mx += 1
                        if self.checkIndexZero2_1 == -1:
                            self.checkIndexZero2_1 = j
                        else:
                            self.checkIndexZero2_2 = j
                    else:
                        self.checkIndexZero4 = j
                        if self.checkIndexZero3_1 == -1:
                            self.checkIndexZero3_1 = j
                        else:
                            self.checkIndexZero3_2 = j
                list.append(self.case(mx, i, en2))

        return list

    def getVertical(self, point, id, guiI):
        list = []
        x = point.get_x()
        y = point.get_y()
        bg = max(0, x - 4)

        i = x
        while i >= bg:
            if guiI.isDifferent(i, y, id):
                bg = i + 1
                break
            if i - 1 < bg: break
            i -= 1

        en = min(guiI.sizeRow - 1, x + 4)
        i = x
        while i <= en:
            if guiI.isDifferent(i, y, id):
                en = i - 1
                break
            if i + 1 > en: break
            i += 1

        if en - bg + 1 >= 5:
            for i in range(bg, x + 1):
                mx = 0
                self.setup()

                en2 = min(guiI.sizeRow - 1, i + 4)
                for k in range(i, en2 + 1):
                    if guiI.isDifferent(k, y, id):
                        en2 = k - 1
                        break

                if en2 > en: break
                # print(" x = ", i, "y = ", y , " enx = " , en2 , " eny = " , y)
                for j in range(i, en2 + 1):
                    if guiI.checked[j][y] == id:
                        mx += 1
                        if self.checkIndexZero2_1 == -1:
                            self.checkIndexZero2_1 = j
                        else:
                            self.checkIndexZero2_2 = j
                    else:
                        self.checkIndexZero4 = j
                        if self.checkIndexZero3_1 == -1:
                            self.checkIndexZero3_1 = j
                        else:
                            self.checkIndexZero3_2 = j
                list.append(self.case(mx, i, en2))
        return list

    def getDiagonalMain(self, point, id, guiI):
        list = []
        x = point.get_x()
        y = point.get_y()

        beg_x = x
        beg_y = y
        time = 4
        # 96->
        while time > 0 and beg_x >= 0 and beg_y >= 0:
            if guiI.isDifferent(beg_x, beg_y, id):
                beg_x += 1
                beg_y += 1
                break
            if beg_x - 1 < 0 or beg_y - 1 < 0: break
            beg_x -= 1
            beg_y -= 1
            time -= 1

        end_x = x
        end_y = y
        time = 4

        while time > 0 and end_x < guiI.sizeRow and end_y < guiI.sizeCol:
            if guiI.isDifferent(end_x, end_y, id):
                end_x -= 1
                end_y -= 1
                break
            if end_x + 1 >= guiI.sizeRow or end_y + 1 >= guiI.sizeCol:
                break
            end_x += 1
            end_y += 1
            time -= 1

        if end_x - beg_x + 1 >= 5:
            i = beg_x
            j = beg_y
            while i <= x and j <= y:
                self.setup()
                mx = 0
                end_x1 = i
                end_y1 = j
                time = 4
                while time > 0 and end_x1 < guiI.sizeRow and end_y1 < guiI.sizeCol:
                    if guiI.isDifferent(end_x1, end_y1, id):
                        end_x1 -= 1
                        end_y1 -= 1
                        break
                    if end_x1 + 1 >= guiI.sizeRow or end_y1 + 1 >= guiI.sizeCol: break
                    end_x1 += 1
                    end_y1 += 1
                    time -= 1
                if end_x1 > end_x: break
                i1 = i
                i2 = j
                while i1 <= end_x1 and i2 <= end_y1:
                    if guiI.checked[i1][i2] == id:
                        mx += 1
                        if self.checkIndexZero2_1 == -1:
                            self.checkIndexZero2_1 = i2
                        else:
                            self.checkIndexZero2_2 = i2
                    else:
                        self.checkIndexZero4 = i2
                        if self.checkIndexZero3_1 == -1:
                            self.checkIndexZero3_1 = i2
                        else:
                            self.checkIndexZero3_2 = i2
                    i1 += 1
                    i2 += 1
                list.append(self.case(mx, j, end_y1))
                i += 1
                j += 1

        return list

    def getDiagonalSecond(self, point, id, guiI):
        list = []
        x = point.get_x()
        y = point.get_y()

        beg_x = x
        beg_y = y
        time = 4

        while time > 0 and beg_x >= 0 and beg_y < guiI.sizeCol:
            if guiI.isDifferent(beg_x, beg_y, id):
                beg_x += 1
                beg_y -= 1
                break
            if beg_x - 1 < 0 or beg_y + 1 >= guiI.sizeCol: break
            beg_x -= 1
            beg_y += 1
            time -= 1

        end_x = x
        end_y = y
        time = 4

        while time > 0 and end_x < guiI.sizeRow and end_y >= 0:
            if guiI.isDifferent(end_x, end_y, id):
                end_x -= 1
                end_y += 1
                break
            if end_x + 1 >= guiI.sizeRow or end_y - 1 < 0:
                break
            end_x += 1
            end_y -= 1
            time -= 1
        if end_x - beg_x + 1 >= 5:
            i = beg_x
            j = beg_y
            while i <= x and j >= y:
                self.setup()
                mx = 0
                end_x1 = i
                end_y1 = j
                time = 4
                while time > 0 and end_x1 < guiI.sizeRow and end_y1 >= 0:
                    if guiI.isDifferent(end_x1, end_y1, id):
                        end_x1 -= 1
                        end_y1 += 1
                        break
                    if end_x1 + 1 >= guiI.sizeRow or end_y1 - 1 < 0:
                        break
                    end_x1 += 1
                    end_y1 -= 1
                    time -= 1
                if end_x1 > end_x: break
                i1 = i
                i2 = j
                while i1 <= end_x1 and i2 >= end_y1:
                    if guiI.checked[i1][i2] == id:
                        mx += 1
                        if self.checkIndexZero2_1 == -1:
                            self.checkIndexZero2_1 = i2
                        else:
                            self.checkIndexZero2_2 = i2
                    else:
                        self.checkIndexZero4 = i2
                        if self.checkIndexZero3_1 == -1:
                            self.checkIndexZero3_1 = i2
                        else:
                            self.checkIndexZero3_2 = i2
                    i1 += 1
                    i2 -= 1
                list.append(self.case(mx, j, end_y1))
                i += 1
                j -= 1

        return list

    def case(self, mx, bg, en):
        if mx == 5:
            return point.Point(mx, 0)
        elif mx == 4:
            return point.Point(mx, self.checkFour(bg, en))
        elif mx == 3:
            return point.Point(mx, self.checkThree(bg, en))
        elif mx == 2:
            return point.Point(mx, self.checkTwo())
        elif mx == 1:
            return point.Point(1, 0)
        else:
            return point.Point(0, 0)

    def checkFour(self, bg, en):
        if self.checkIndexZero4 == bg or self.checkIndexZero4 == en:
            return 0
        return 1

    def checkThree(self, bg, en):
        # print(self.checkIndexZero3_1, " ", self.checkIndexZero3_2)
        # print(bg, " ", en)
        # check sai roi
        if self.checkIndexZero3_1 == bg and self.checkIndexZero3_2 == en:
            return 0
        if abs(self.checkIndexZero3_1 - self.checkIndexZero3_2) == 1:
            if self.checkIndexZero3_1 == bg or self.checkIndexZero3_2 == en:
                return 0
        return 1

    def checkTwo(self):
        if abs(self.checkIndexZero2_1 - self.checkIndexZero2_2) == 1:
            return 0
        return 1

    def setup(self):
        self.checkIndexZero4 = -1
        self.checkIndexZero3_1 = -1
        self.checkIndexZero3_2 = -1
        self.checkIndexZero2_1 = -1
        self.checkIndexZero2_2 = -1


if __name__ == '__main__':
    ex = Experience()
    guiI = Gui.GuiInterface()
    guiI.checked[4][7] = 1
    guiI.checked[4][6] = 1
    guiI.checked[6][4] = 1
    guiI.checked[7][4] = 1



    # guiI.memory.append([6, 6])

    print(guiI.checked)

    # guiI.checked[1][8] = 1
    # guiI.checked[2][9] = 0
    # guiI.checked[3][10] = 1
    print(ex.defen(point.Point(4 , 4) , 1 , guiI))
