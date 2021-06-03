import numpy as np

import Gui
import HeuristicAtPoint
import Player as pl
import Point as point


class Information:
	numRight = 0
	numDown = 0
	numDownR = 0
	numDownL = 0

	def __init__(self, numRight, numDown, numDownR, numDownL):
		self.numRight = numRight
		self.numDown = numDown
		self.numDownR = numDownR
		self.numDownL = numDownL

	def getNumberRight(self):
		return self.numRight

	def getNumberDown(self):
		return self.numDown

	def getNumberDownRight(self):
		return self.numDownR

	def getNumberDownLeft(self):
		return self.numDownL


class Experience:

	def think(self, id, guiI):
		list = self.listWays(guiI, id)

		sum = -1
		for i in range(len(list)):
			# print(list[i].getNumberRight() , list[i].getNumberDown() , list[i].getNumberDownRight() , list[i].getNumberDownLeft())
			w = self.setUpArr(list[i])
			sumObj = self.getSumArr(w)
			if sumObj > sum:
				sum = sumObj
			if sum >= pl.Score.line5:
				break

		sz = len(guiI.memory)
		x = guiI.memory[sz - 1][0]
		y = guiI.memory[sz - 1][1]
		# if guiI.checked[x][y] == id:
			# sumDefen = self.defen(point.Point(x, y), id, guiI)
			# sum = max(sum, sumDefen)
			# sum += sumDefen

		return sum

	def defen(self, newPoint, id, guiI):
		defen = HeuristicAtPoint.Experience().getDefen(newPoint, id, guiI)

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
					if w[i] >= 1 and w[j] >= 1: # i > j
						w[i + 1] += 1
						w[i] = 0
						w[j + 1] += 1
						w[j] = 0
				j -= 1
			i -= 1

		sumAtPoint = self.getSumArr(w, flag=False)
		return sumAtPoint

	def listWays(self, guiI, id):
		list = []

		for i in range(len(guiI.memory)):
			x = guiI.memory[i][0]
			y = guiI.memory[i][1]
			newPoint = point.Point(x, y)
			if guiI.checked[x][y] == id:
				right = self.getNumberRight(newPoint, guiI, id)
				down = self.getNumberDown(newPoint, guiI, id)
				downR = self.getNumberDownRight(newPoint, guiI, id)
				downL = self.getNumberDownLeft(newPoint, guiI, id)
				list.append(Information(right, down, downR, downL))

		return list

	def getSumArr(self, w, flag=True):
		if flag:
			return w[1] + w[2] * pl.Score.line2 + w[3] * pl.Score.line3 + w[4] * pl.Score.line4 + w[5] * pl.Score.line5
		else:
			return w[1] + w[2] * pl.Score.line2D + w[3] * pl.Score.line3D + w[4] * pl.Score.line4D + w[
				5] * pl.Score.line5D

	def setUpArr(self, infor):
		w = np.array([0, 0, 0, 0, 0, 0], dtype=int)
		list = np.array(
			[0, infor.getNumberRight(), infor.getNumberDown(), infor.getNumberDownRight(), infor.getNumberDownLeft()],
			dtype=int)
		for i in range(len(list)):
			if list[i] == 0:
				continue
			else:
				w[list[i]] = w[list[i]] + 1
		return w

	def setUpArrDefen(self, list):
		w = np.array([0, 0, 0, 0, 0, 0], dtype=int)
		for i in range(len(list)):
			if list[i] == 0:
				continue
			else:
				w[list[i]] = w[list[i]] + 1
		return w

	def getNumberDownLeft(self, newPoint, guiI, id):
		numDownL = 0
		space = 0
		x = newPoint.x
		y = newPoint.y
		end = -1
		nextX = min(x + 4, guiI.sizeRow - 1)
		nextY = max(y - 4, 0)
		# find end in downL
		i, j = x, y
		while i <= nextX and j >= nextY:
			if guiI.isDifferent(i, j, id):
				end = i
				break
			if guiI.checked[i][j] == id:
				numDownL += 1
			else:
				space += 1
			i += 1
			j -= 1

		# have 5 line
		if end == -1 and numDownL + space == 5:
			return numDownL
		# no 5 line
		# check up
		i, j = x - 1, y + 1
		canMove = False
		add = 0
		while i >= 0 and j < guiI.sizeRow:
			if guiI.isDifferent(i, j, id):
				break
			add += 1
			if numDownL + space + add == 5:
				canMove = True
				break
			i -= 1
			j += 1
		if canMove:
			return numDownL
		else:
			return 0

	def getNumberDownRight(self, newPoint, guiI, id):
		numDownR = 0
		space = 0
		x = newPoint.x
		y = newPoint.y
		end = -1
		nextX = min(x + 4, guiI.sizeRow - 1)
		nextY = min(y + 4, guiI.sizeCol - 1)
		# find end in downR
		i, j = x, y
		while i <= nextX and j <= nextY:
			if guiI.isDifferent(i, j, id):
				end = i
				break
			if guiI.checked[i][j] == id:
				numDownR += 1
			else:
				space += 1
			i += 1
			j += 1

		# have 5 line
		if end == -1 and numDownR + space == 5:
			return numDownR
		# no 5 line
		# check up
		i, j = x - 1, y - 1
		canMove = False
		add = 0
		while i >= 0 and j >= 0:
			if guiI.isDifferent(i, j, id):
				break
			add += 1
			if numDownR + space + add == 5:
				canMove = True
				break
			i -= 1
			j -= 1
		if canMove:
			return numDownR
		else:
			return 0

	def getNumberDown(self, newPoint, guiI, id):
		numDown = 0
		space = 0
		x = newPoint.x
		y = newPoint.y
		end = -1
		next = min(x + 4, guiI.sizeRow - 1)
		# find end in down
		for i in range(x, next + 1):
			if guiI.isDifferent(i, y, id):
				end = i
				break
			elif guiI.checked[i][y] == id:
				numDown += 1
			else:
				space += 1
		# have 5 line
		if end == -1 and numDown + space == 5:
			return numDown
		# no 5 line
		# check left
		i = x - 1
		canMove = False
		add = 0
		while i >= 0:
			if guiI.isDifferent(i, y, id):
				break
			add += 1
			if space + numDown + add == 5:
				canMove = True
				break
			i -= 1
		if canMove:
			return numDown
		else:
			return 0

	def getNumberRight(self, newPoint, guiI, id):
		numRight = 0
		space = 0
		x = newPoint.x
		y = newPoint.y
		end = -1
		next = min(y + 4, guiI.sizeCol - 1)
		# find end in right
		for i in range(y, next + 1):
			if guiI.isDifferent(x, i, id):
				end = i
				break
			elif guiI.checked[x][i] == id:
				numRight += 1
			else:
				space += 1
		# have 5 line
		if end == -1 and numRight + space == 5:
			return numRight
		# no 5 line
		# check left
		i = y - 1
		canMove = False
		add = 0
		while i >= 0:
			if guiI.isDifferent(x, i, id):
				break
			add += 1
			if space + numRight + add == 5:
				canMove = True
				break
			i -= 1
		if canMove:
			return numRight
		else:
			return 0


def main():
	ex = Experience()
	guiI = Gui.GuiInterface()
	guiI.checked[6][6] = 1
	guiI.checked[7][5] = 1
	guiI.checked[8][4] = 1
	guiI.checked[9][3] = 1
	guiI.checked[5][6] = 1
	guiI.checked[5][8] = 1


	guiI.memory.append([5, 7])

	print(guiI.checked)

	# guiI.checked[1][8] = 1
	# guiI.checked[2][9] = 0
	# guiI.checked[3][10] = 1
	print(ex.defen(point.Point(5 , 7) , 2 , guiI))


if __name__ == '__main__':
	main()
