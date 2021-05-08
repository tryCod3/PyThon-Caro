class EntityPlayer:
    user = 2
    ai = 1
    win = False
    noOneHasLost = False
    realNext = 1
    vsUser = None


class Score:
    line5 = 1e7
    line4 = 1e6 + (1e5 * 2)
    line3 = 1e5
    line2 = 1e2
