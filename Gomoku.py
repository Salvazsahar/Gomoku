import math


#CHECKWIN V2 IS NEXT, NO NEED FOR BOARDS ONLY ROW COLUMN AND 2 DIAGONALS
#CHECKWIN V2 IS NEXT, NO NEED FOR BOARDS ONLY ROW COLUMN AND 2 DIAGONALS
#CHECKWIN V2 IS NEXT, NO NEED FOR BOARDS ONLY ROW COLUMN AND 2 DIAGONALS
#CHECKWIN V2 IS NEXT, NO NEED FOR BOARDS ONLY ROW COLUMN AND 2 DIAGONALS
#CHECKWIN V2 IS NEXT, NO NEED FOR BOARDS ONLY ROW COLUMN AND 2 DIAGONALS
#CHECKWIN V2 IS NEXT, NO NEED FOR BOARDS ONLY ROW COLUMN AND 2 DIAGONALS
#CHECKWIN V2 IS NEXT, NO NEED FOR BOARDS ONLY ROW COLUMN AND 2 DIAGONALS
#CHECKWIN V2 IS NEXT, NO NEED FOR BOARDS ONLY ROW COLUMN AND 2 DIAGONALS
#CHECKWIN V2 IS NEXT, NO NEED FOR BOARDS ONLY ROW COLUMN AND 2 DIAGONALS
#CHECKWIN V2 IS NEXT, NO NEED FOR BOARDS ONLY ROW COLUMN AND 2 DIAGONALS


def update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size):
    br1 = boardrow + []
    bc1 = boardcolumn + []
    bdr1 = boarddiaright + []
    bdl1 = boarddialeft + []
    print "row", r, "column", c
    #print "AAAAAAAA", "dia right", bdr1[r+c], "dia left", bdl1[c+size-r-1], "row", br1[r], "column", bc1[c]
    br1[r] += color << 2 * c
    bc1[c] += color << 2 * r
    # Right Diagonal
    s = [0]
    if r + c +1> size:
        bdr1[r + c] += color << 2 * (size-r-1)
    else:
        bdr1[r + c] += color << 2 * c
    # Left Diagonal
    if c + size - r > size:
        bdl1[(c + size - r) - 1] += color << 2 * r
    else:
        bdl1[(c + size - r) - 1] += color << 2 * c
    # print "BBBBBBBB", "dia right", bdr1[r+c], "dia left", bdl1[c+size-r-1], "row", br1[r], "column", bc1[c]
    if br1[r] > 63:
        s[1] = 1
    return br1, bc1, bdr1, bdl1


def checkwin(count, row, column, boarddiaright, boarddialeft, boardrow, boardcolumn, size):
    mask = 21
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


def gomokupvp(count, turn, boarddiaright, boarddialeft, boardrow, boardcolumn, size):
    color = 3-(turn & 1)
    cc = 0
    while cc == 0:
        cc = 1
        r = int(raw_input("Enter the row you wish to place in, player " + str(turn & 1) + " : "))
        c = int(raw_input("Enter the column you wish to place in, player " + str(turn & 1) + " : "))
        # ROW
        maskr = (1 << 2*(c))
        if boardrow[r] & maskr*3 == maskr*2 or boardrow[r] & maskr*3 == maskr*3:
            cc = 0
        else:
            boardrow[r] += (1 << 2*(c))*color
        if cc == 1:
            # Column
            boardcolumn[c] += (1 << 2*(r)) * color
            # Right Diagonal
            if r+c + 1 > size:
                boarddiaright[(r+c+1) - 1] += (1 << 2*(c-(r+c-size)-1)) * color
            else:
                boarddiaright[(r+c+1)-1] += (1 << 2*(c)) * color
            # Left Diagonal
            if c+size-r > size:
                boarddialeft[(c+size-r) - 1] += (1 << 2*(r)) * color
            else:
                boarddialeft[(c+size-r)-1] += (1 << 2*(c)) * color
            # End Placement
        else:
            print "Try Again"
    printboardrow(boardrow)
    print "dialeft", boarddialeft, "diaright", boarddiaright, "row", boardrow, "column", boardcolumn
    win = checkwin(count, r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
    if win == 1:
        print "player 1 has won"
        return 1
    elif win == -1:
        print "player 2 has won"
        return -1
    return 0


def basic_mm_gomoku(count, color, boarddiaright, boarddialeft, boardrow, boardcolumn, boardpavailable, size, depth, remaining):
    print "entering: depth =", depth, ", remaining =", remaining
    printboardrow(boardrow)
    bestrow = 0
    bestcolumn = 0
    best = -1 if color == 2 else 1
 #   print "MMMMMMMMMM", "dia right", boarddiaright, "dia left", boarddialeft, "row", boardrow, "column", boardcolumn
    for r in range (0, size):
        rowavailable = boardpavailable[r]
        flag = 0
        while rowavailable != 0 and flag == 0:
            place = 1
            c = 0
            while rowavailable & place == 0:
                place <<= 2
                c += 1
#            print "AAAAAAA", "row", r, "column after change", c, "place", place, "row available", rowavailable
            rowavailable ^= place
#            print "BBBBBBB", "row", r, "column after change", c, "place", place, "row available", rowavailable
#            print "GGGGGGGGG", "dia right", boarddiaright, "dia left", boarddialeft, "row", boardrow, "column", boardcolumn
#            print "CCCCCCCCC", "dia right", boarddiaright[r + c], "dia left", boarddialeft[c + size - r - 1], "row", boardrow[r], "column", boardcolumn[c]
            br1, bc1, bdr1, bdl1 = update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
#            print "LLLLLLLLL", "dia right", bdr1, "dia left", bdl1, "row", br1, "column", bc1
#            print "DDDDDDDDD", "dia right", bdr1[r + c], "dia left", bdl1[c + size - r - 1], "row", br1[r], "column", bc1[c]
            w = checkwin(count, r, c, bdr1, bdl1, br1, bc1, size)
            print "w = ", w, ", c = ", c, ", r = ", r
            if w == 0:
                boardpavailable2 = boardpavailable + []
                boardpavailable2[r] ^= place
                if remaining > 1:
                    w, row, column = basic_mm_gomoku(count, color^1, bdr1, bdl1, br1, bc1, boardpavailable2, size, depth+1, remaining-1)
                    print "win, row, column", w, row, column
            else:
                flag = 1
                print "WIN WIN WIN"
            if (color == 3 and w < best) or (color == 2 and w > best):
                best = w
                bestrow = r
                bestcolumn = c
                print "bestRow", bestrow, "bestColumn", bestcolumn
    printboardrow(boardrow)
    print "exiting: depth =", depth, best, bestrow, bestcolumn
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
                print "board -", boardpavailable,"num -",boardpavailable[r],"equal -",boardpavailable[r] & place,"place",place
                print "Try Again"
                r = int(raw_input("Enter the row you wish to place in, player " + str(turn & 1) + " : "))
                c = int(raw_input("Enter the column you wish to place in, player " + str(turn & 1) + " : "))
                place = 1 << 2 * (c)
            boardpavailable[r] ^= place
            # print "EEEEEEEEEE", "dia right", boarddiaright[r + c], "dia left", boarddialeft[c + size - r - 1], "row", boardrow[r], "column", boardcolumn[c]
            boardrow, boardcolumn, boarddiaright, boarddialeft = update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size) # Updating the boards.
            # print "FFFFFFFFFF", "dia right", boarddiaright[r + c], "dia left", boarddialeft[c + size - r - 1], "row", boardrow[r], "column", boardcolumn[c]
            win = checkwin(count, r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
            print "win p1 =", win
            if win == 1:
                print "You have won"
                flag == 1
        else:
            color = 3
            # print "GGGGGGGG", "dia right", boarddiaright[r + c], "dia left", boarddialeft[c + size - r - 1], "row", boardrow[r], "column", boardcolumn[c]
            s, r, c = basic_mm_gomoku(count, color, boarddiaright, boarddialeft, boardrow, boardcolumn, boardpavailable, size,0, remaining)
            print "computer places here: \n", "Row: ", r, "Column: ",c
            place = 1 << 2 * (c)
            boardpavailable[r] ^= place
            boardrow, boardcolumn, boarddiaright, boarddialeft = update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size) # Updating the boards.
            win = checkwin(count, r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
            print "win p2 =", win
            if win == -1:
                print "The Computer Has Won"
                flag = -1
        turn +=1
        remaining -= 1


def exmixtrixreal(board1, turn, listwin1, placesavailable):
    flag = 0
    while (placesavailable != 0 and flag == 0):
        printboard(board1)
        if turn & 1 == 1:
            print turn, " - ", turn & 1
            place = int(raw_input("Enter the place in which you wish to place the X: "))
            place = 1 << 2 * place
            while placesavailable & place != place:
                place = int(raw_input("try again: "))
                place = 1 << 2 * place
            board1 += place * 2
            placesavailable = placesavailable ^ place
            win = checkwin(board1, listwin1)
            if win == 1:
                print "you have defeated the computer"
                flag = 1
        else:
            print "a"
            s,p = exmixtrix1(board1,3,listwin1,placesavailable)
            print "i choose to place here:", p
            board1 += p*3
            placesavailable ^= p
            if checkwin(board1,listwin1) == -1:
                print "the computer has beaten you"
                flag = -1
        turn += 1
    if flag == 0:
        print "it was a draw"






boardrow1 = [0, 0, 0]
boardcolumn1 = [0, 0, 0]
boarddiaright1 = [0, 0, 0, 0, 0]
boarddialeft1 = [0, 0, 0, 0, 0]
boardpavailable1 = [21, 21, 21]
size1 = 3
count1 = 3
turn1 = 1
mm_vs_player_gomoku(count1, boarddiaright1, boarddialeft1, boardrow1, boardcolumn1, boardpavailable1, size1, turn1)
# w1 = gomokupvp(count1, turn1, boarddiaright1, boarddialeft1, boardrow1, boardcolumn1, size1)
# i = 0
# while(w1==0 and i<(size1*size1)):
    # turn1 +=1
    # w1 = gomokupvp(count1, turn1, boarddiaright1, boarddialeft1, boardrow1, boardcolumn1, size1)
    # i+=1




