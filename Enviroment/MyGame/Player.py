class EntityPlayer:
	user = 2
	ai = 1
	win = False
	noOneHasLost = False
	realNext = 1
	vsUser = None


class Score:
	line5 = 1e7
	line4 = 1e5
	line3 = 1e3
	line2 = 1e1

	line5D = 1e7
	line4D = 1e5 // 2 + 1
	line3D = 1e3 // 2 + 1
	line2D = 1e1 // 2 + 1
