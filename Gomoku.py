import math


def checkwin(count ,row, column, boarddiaright, boarddialeft, boardrow, boardcolumn, size):
    mask = 85
    low = max(column - count, 0)
    high = min(size - 1, column + count - 2)
    num = boardrow[row - 1]
    while (low <= high - count + 1):
        if (num >> 2*low) & mask*3 == mask*2:
            return 1
        elif (num >> 2 * low) & mask * 3 == mask * 3:
            return -1
        low += 1
    ##########
    low = max(row - count, 0)
    high = min(size - 1, row + count - 2)
    num = boardcolumn[column - 1]
    while (low <= high - count + 1):
        if (num >> 2 * low) & mask * 3 == mask * 2:
            return 1
        elif (num >> 2 * low) & mask * 3 == mask * 3:
            return -1
        low += 1
    ##########1
    if row + column - 1 > size:
        low = max((column - (row + column - 1 - size) - count), 0)
        high = min((column - (row + column - 1 - size) + count-2), row - 1 - 1)
    else:
        low = max((column - count), 0)
        high = min((column + count-2), column - 1)
    num = boarddiaright[(row + column - 1) - 1]
    while (low <= high - count + 1):
        if (num >> 2 * low) & mask * 3 == mask * 2:
            return 1
        elif (num >> 2 * low) & mask * 3 == mask * 3:
            return -1
        low += 1
    ##########
    if column > row:
        low = max((row - count), 0)
        high = min((row + count - 2), size - column + row - 1)
    else:
        low = max((column - count), 0)
        high = min((column + count - 2), size - row + column - 1)
    num = boarddialeft[(column + size - row) - 1]
    print num, low, high
    while low <= high - (count-1):
        if (num >> (2*low)) & (mask*3) == mask * 2:
            return 1
        elif (num >> (2 * low)) & (mask * 3) == mask * 3:
            return -1
        low += 1
    return 0


def buildboardrowandcolumn(size):
    boardrc = []
    for i in xrange(size):
        num = 0
        for j in xrange(size):
            num += 1<<2*j
        boardrc.append(num)
    return boardrc


def builboarddia(size):
    boarddia = []
    for i in xrange(1,size**2):
        j = 0
        num = 0
        if i<=size:
            while (j<=i):
                num += 1<<2*j
                j += 1
        else:
            while(j<= (size*2-i)):
                num += 1<<2*j
                j += 1
        boarddia.append(num)
    return boarddia


def printboardrow(boardrow):
    for i in boardrow:
        for j in range (len(boardrow)):
            a = i & 3
            if a == 3:
                print "o",
            elif a == 2:
                print "x",
            else:
                print ".",
            i >>= 2
        print



def gomokupvp (count, turn, boarddiaright, boarddialeft, boardrow, boardcolumn, size):
    color = 3-(turn&1)
    r = int(raw_input("Enter the row you wish to place in, player " + str(turn&1) + " : "))
    c = int(raw_input("Enter the column you wish to place in, player " + str(turn&1) + " : "))
    boardrow[r-1] += (1<<2*(c-1)) * color
    boardcolumn[c-1] += (1<<2*(r-1)) * color
    if r+c-1 > size:
        boarddiaright[(r + c - 1) - 1] += (1<<2*(c-(r+c-1-size)-1)) * color
    else:
        boarddiaright[(r+c-1)-1] += (1<<2*(c-1)) * color
    if c+size-r > size:
        boarddialeft[(c + size - r) - 1] += (1<<2*(r-1)) * color
    else:
        boarddialeft[(c+size-r)-1] += (1<<2*(c-1)) * color
    printboardrow(boardrow)
    print boarddialeft
    win = checkwin(count ,r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
    print "b"
    if win == 1:
        print "player 1 has won"
        return 1
    elif win == -1:
        print "player 2 has won"
        return -1
    return 0

boardrow = [0,0,0,0,0]
boardcolumn = [0,0,0,0,0]
boarddiaright = [0,0,0,0, 0 ,0,0,0,0]
boarddialeft = [0,0,0,0, 0 ,0,0,0,0]
size = 5
count = 4
turn = 1
win = gomokupvp (count, turn, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
while win == 0:
    turn += 1
    win = gomokupvp(count, turn, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
    print "a"
