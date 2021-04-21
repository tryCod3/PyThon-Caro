import Point as point
import Gui

arrAttack = [
    [0, 0],
    [1, 0],
    [200, 100],
    [20000, 200],
    [100000, 200],
    [10000000, 10000000]
]



class Experience:

    def think(self, id, guiI):
        sum = 0
        sz = len(guiI.memory)
        for i in range(sz):
            x = guiI.memory[i][0]
            y = guiI.memory[i][1]
            if guiI.checked[x][y] == id:
                newPoint = point.Point(x, y)
                sum += self.attack(newPoint, id, guiI)
        return sum

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
                            self.checkIndexZero3_1 = j
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
                            self.checkIndexZero3_1 = i2
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


def main():
    ex = Experience()
    guiI = Gui.GuiInterface()
    guiI.checked[0][7] = 1
    guiI.checked[1][7] = 0
    guiI.checked[2][7] = 1
    guiI.checked[3][7] = 1
    guiI.checked[4][7] = 0
    guiI.checked[1][8] = 1
    guiI.checked[2][9] = 0
    guiI.checked[3][10] = 1
    print(ex.attack(point.Point(0, 7), 1, guiI))


if __name__ == '__main__':
    main()
