import math


def update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size):
    boardrow[r] ^= color << 2 * c
    boardcolumn[c] ^= color << 2 * r
    if r + c + 1 > size:
        boarddiaright[r + c] ^= color << 2 * (size-r-1)
    else:
        boarddiaright[r + c] ^= color << 2 * c
    if c + size - r > size:
        boarddialeft[(c + size - r) - 1] ^= color << 2 * r
    else:
        boarddialeft[(c + size - r) - 1] ^= color << 2 * c


def checkwin(count, row, column, boarddiaright, boarddialeft, boardrow, boardcolumn, size):
    mask = 85
    low = max(column - count+1, 0)
    high = min(size - 1, column + count - 1)
    num = boardrow[row]
    while low <= high - count + 1:
        if (num >> 2*low) & mask*3 == mask*2:
            return 1
        elif (num >> 2 * low) & mask * 3 == mask * 3:
            return -1
        low += 1
    ##########
    low = max(row - count + 1, 0)
    high = min(size - 1, row + count - 1)
    num = boardcolumn[column]
    while low <= high - count + 1:
        if (num >> 2 * low) & mask * 3 == mask * 2:
            return 1
        elif (num >> 2 * low) & mask * 3 == mask * 3:
            return -1
        low += 1
    # #########1
    if row + column + 1 > size:
        low = max((column - (row + column - size) - count), 0)
        high = min((column - (row + column - size) + count-2), size*2-(row+column+2))
    else:
        low = max((column - count + 1), 0)
        high = min((column + count - 1), row+column)
    num = boarddiaright[(row + column + 1) - 1]
    while low <= high - count + 1:
        if (num >> 2 * low) & mask * 3 == mask * 2:
            return 1
        elif (num >> 2 * low) & mask * 3 == mask * 3:
            return -1
        low += 1
    ##########
    if column > row:
        low = max((row - count + 1), 0)
        high = min((row + count - 1), size - column + row - 1)
    else:
        low = max((column - count + 1), 0)
        high = min((column + count - 1), size - row + column - 1)
    num = boarddialeft[(column + size - row) - 1]
    while low <= high-count+1:
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
            num += 1 << 2*j
        boardrc.append(num)
    return boardrc


def builboarddia(size):
    boarddia = []
    for i in xrange(1, size**2):
        j = 0
        num = 0
        if i <= size:
            while j <= i:
                num += 1 << 2*j
                j += 1
        else:
            while j <= (size*2-i):
                num += 1 << 2*j
                j += 1
        boarddia.append(num)
    return boarddia


def printboardrow(boardrow):
    for i in boardrow:
        for j in range(len(boardrow)):
            a = i & 3
            if a == 3:
                print "o",
            elif a == 2:
                print "x",
            else:
                print ".",
            i >>= 2
        print
        

def basic_mm_gomoku(count, color, boarddiaright, boarddialeft, boardrow, boardcolumn, boardpavailable, size, depth, remaining):
    bestrow = 0
    bestcolumn = 0
    best = -1 if color == 2 else 1
    flag = 0
    count1 = 0
    for r in range (0, size):
        rowavailable = boardpavailable[r]
        while rowavailable != 0 and flag == 0:
            place = 1
            c = 0
            while rowavailable & place == 0:
                place <<= 2
                c += 1    
            rowavailable ^= place
            update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
            w = checkwin(count, r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
            if w == 0:
                if remaining > 1 and depth<3:
                    count1+=1
                    boardpavailable[r] ^= place
                    w, row, column = basic_mm_gomoku(count, color^1, boarddiaright, boarddialeft, boardrow, boardcolumn, boardpavailable, size, depth+1, remaining-1)
                    boardpavailable[r]^= place
            else:
                flag = 1
#                print "WIN WIN WIN"
            update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
            if (color == 3 and w <= best) or (color == 2 and w >= best):
                best = w
                bestrow = r
                bestcolumn = c
        if rowavailable != 0 and flag != 1:
            print "available", rowavailable, "flag", flag
    return best, bestrow, bestcolumn


def mm_vs_player_gomoku(count, boarddiaright, boarddialeft, boardrow, boardcolumn, boardpavailable, size, turn): # R is inputed as 0
    flag = 0
    remaining = size*size
    while (turn <= size**2 and flag == 0):
        printboardrow(boardrow)
        print "my board", boardrow
        if turn & 1 == 1:
            color = 2
            r = int(raw_input("Enter the row you wish to place in, player " + str(turn & 1) + " : "))
            c = int(raw_input("Enter the column you wish to place in, player " + str(turn & 1) + " : "))
            place = 1 << 2*(c)
            while boardpavailable[r] & place == 0:
                print "Try Again"
                r = int(raw_input("Enter the row you wish to place in, player " + str(turn & 1) + " : "))
                c = int(raw_input("Enter the column you wish to place in, player " + str(turn & 1) + " : "))
                place = 1 << 2 * (c)
            boardpavailable[r] ^= place
            # print "EEEEEEEEEE", "dia right", boarddiaright[r + c], "dia left", boarddialeft[c + size - r - 1], "row", boardrow[r], "column", boardcolumn[c]
            update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size) # Updating the boards.
            win = checkwin(count, r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
            print "win p1 =", win
            if win == 1:
                print "You have won"
                flag == 1
        else:
            color = 3
            s, r, c = basic_mm_gomoku(count, color, boarddiaright, boarddialeft, boardrow, boardcolumn, boardpavailable, size,0, remaining)
            print "computer places here: \n", "Row: ", r, "Column: ",c
            place = 1 << 2 * (c)
            boardpavailable[r] ^= place
            update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size) # Updating the boards.
            win = checkwin(count, r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
            print "win p2 =", win
            if win == -1:
                print "The Computer Has Won"
                flag = -1
        turn +=1
        remaining -= 1



boardrow1 = [0, 0, 0, 0, 0]
boardcolumn1 = [0, 0, 0, 0, 0]
boarddiaright1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
boarddialeft1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
boardpavailable1 = [341, 341, 341, 341, 341]
size1 = 5
count1 = 4
turn1 = 1
mm_vs_player_gomoku(count1, boarddiaright1, boarddialeft1, boardrow1, boardcolumn1, boardpavailable1, size1, turn1)









