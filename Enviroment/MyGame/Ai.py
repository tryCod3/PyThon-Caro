import sys
import threading
import time

import Heuristic
import HeuristicAtPoint
import Player as pl
import Point as point
import State as st


class Resurt:
	x = 0
	y = 0
	score = 0

	def __init__(self, x, y, score):
		self.x = x
		self.y = y
		self.score = score


class Play(threading.Thread):

	def __init__(self, condition, condition_choise, guiI, event):
		threading.Thread.__init__(self)
		self.condition = condition
		self.condition_choise = condition_choise
		self.guiI = guiI
		self.event = event

	def movePoint(self, move, id):
		if id == pl.EntityPlayer.ai:
			c = 'O'
		else:
			c = 'X'
		point = move.bestMove()
		x = point.get_x()
		y = point.get_y()
		self.guiI.setArrButton(x, y, c)
		self.guiI.memory.append([x, y])
		self.guiI.checked[x][y] = id
		self.guiI.changeColor()

	def vsUser(self):
		move = Move(self.guiI)
		try:
			while pl.EntityPlayer.realNext == pl.EntityPlayer.ai and pl.EntityPlayer.win == pl.EntityPlayer.noOneHasLost:
				self.movePoint(move, pl.EntityPlayer.ai)
				pl.EntityPlayer.realNext = pl.EntityPlayer.user
				if st.hasWin(pl.EntityPlayer.ai, self.guiI):
					pl.EntityPlayer.win = True
					self.event.notification("Winner for ", 'O')
					break
				print("watting player move...")
				self.condition.clear()
				self.condition.wait()
		except:
			print("error at class Ai in method run")
			raise
		pl.EntityPlayer.realNext = pl.EntityPlayer.user

	def vsAi(self):
		print("ai")
		move = Move(self.guiI)
		while pl.EntityPlayer.win == False:
			try:
				time.sleep(0.5)
				print("ai move")
				self.movePoint(move, pl.EntityPlayer.ai)
				if st.hasWin(pl.EntityPlayer.ai, self.guiI):
					self.event.notification("Winner for ", 'O')
					break
				time.sleep(0.5)
				print("watting player move...")
				self.movePoint(move, pl.EntityPlayer.user)
				if st.hasWin(pl.EntityPlayer.user, self.guiI):
					self.event.notification("Winner for ", 'X')
					break
			except:
				print("error at class Ai in method run")
				raise
		pl.EntityPlayer.realNext = pl.EntityPlayer.user

	def run(self):

		while True:
			self.condition_choise.clear()
			self.condition_choise.wait()

			if pl.EntityPlayer.vsUser:
				self.vsUser()
			else:
				self.vsAi()


class Move:
	heu = Heuristic.Experience()
	HeuAtPoint = HeuristicAtPoint.Experience()

	max_int = sys.maxsize
	min_int = -sys.maxsize

	def __init__(self, guiI):
		self.guiI = guiI

	def bestMove(self):

		if st.isFullBoard(self.guiI) == False:
			depth = self.setCaseDepth()
			print("depth = ", depth)
			curPlay = st.whoNext(self.guiI)
			if len(self.guiI.memory) == 0:
				return point.Point(self.guiI.sizeRow // 2, self.guiI.sizeCol // 2)
			else:
				re = self.minimaxAlphaBeta(depth, self.min_int, self.max_int, curPlay)
				print("score = " , re.score)
				return point.Point(re.x, re.y)
		else:
			print("isFull")

	def sortList(self, list, id, method):
		global att
		sz = len(list)
		listResurt = []
		for i in range(sz):
			x = list[i].x
			y = list[i].y
			self.guiI.checked[x][y] = id
			self.guiI.memory.append([x, y])
			if method == "think":
				att = self.HeuAtPoint.think(id, self.guiI)
			elif method == "attack":
				att = self.HeuAtPoint.attack(point.Point(x, y), id, self.guiI)
			listResurt.append(Resurt(x, y, att))
			self.guiI.checked[x][y] = 0
			self.guiI.memory.pop()
		if len(listResurt) > 0:
			listResurt.sort(key=lambda x: x.score, reverse=True)
		return listResurt

	def setCaseDepth(self):

		list = st.listCanGo(self.guiI)
		listAi = self.sortList(list, pl.EntityPlayer.ai, "think")
		listUser = self.sortList(list, pl.EntityPlayer.user, "think")



		mx = 0
		if len(listAi) > 0 or len(listUser) > 0:
			if len(listAi) == 0:
				mx = listUser[0].score
			if len(listUser) == 0:
				mx = listAi[0].score
			else:
				mx = max(listAi[0].score, listUser[0].score)

			if mx >= pl.Score.line5:
				return 2
			else:
				return 3

		else:
			return 0

	def minimaxAlphaBeta(self, depth, alpha, beta, isAi):
		isWinAi = self.heu.think(pl.EntityPlayer.ai, self.guiI)
		isWinUser = self.heu.think(pl.EntityPlayer.user, self.guiI)

		isFull = st.isFullBoard(self.guiI)
		isDethpZero = depth

		list = st.listCanGo(self.guiI)
		sz = len(list)

		if sz == 0 or isWinAi >= pl.Score.line5 or isWinUser >= pl.Score.line5 or isFull or isDethpZero == 0:
			if isWinAi == 0: isWinAi = 1
			if isWinUser == 0: isWinUser = 1
			if isAi == pl.EntityPlayer.ai:
				isWinAi = isWinAi * pow(2 , 1)
			else:
				isWinUser = isWinUser * pow(2 , 3)
			value = isWinAi - isWinUser
			if value > 0:
				value += depth
			elif value < 0:
				value -= depth
			return Resurt(0, 0, value)

		sortList = self.sortList(list, pl.EntityPlayer.ai, "attack")

		# for i in range(len(sortList)):
		# 	print(sortList[i].x , " " ,  sortList[i].y , " " , sortList[i].score)

		if isAi == pl.EntityPlayer.ai:
			bestMove = Resurt(0, 0, self.min_int)
			szSl = len(sortList)
			for i in range(szSl):
				x = sortList[i].x
				y = sortList[i].y
				self.guiI.checked[x][y] = 1
				self.guiI.memory.append([x, y])
				tmp = self.minimaxAlphaBeta(depth - 1, alpha, beta, pl.EntityPlayer.user)
				self.guiI.checked[x][y] = 0
				self.guiI.memory.pop()
				if tmp.score > bestMove.score:
					tmp.x = x
					tmp.y = y
					bestMove = tmp
				if bestMove.score >= beta:
					return Resurt(bestMove.x, bestMove.y, bestMove.score)
				alpha = max(alpha, bestMove.score)
				if alpha >= beta: break
			return bestMove
		else:
			bestMove = Resurt(0, 0, self.max_int)
			szSl = len(sortList)
			for i in range(szSl):
				x = sortList[i].x
				y = sortList[i].y
				self.guiI.checked[x][y] = 2
				self.guiI.memory.append([x, y])
				tmp = self.minimaxAlphaBeta(depth - 1, alpha, beta, pl.EntityPlayer.ai)
				self.guiI.checked[x][y] = 0
				self.guiI.memory.pop()
				if tmp.score < bestMove.score:
					tmp.x = x
					tmp.y = y
					bestMove = tmp
				if bestMove.score <= alpha:
					return Resurt(bestMove.x, bestMove.y, bestMove.score)
				beta = min(beta, bestMove.score)
				if alpha >= beta: break
			return bestMove
