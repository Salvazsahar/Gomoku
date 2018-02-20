from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from functools import partial
import math


def score(count, row, column, boarddiaright, boarddialeft, boardrow, boardcolumn, size, color):
    totscore = 0
    ##########
    low = max(column - count + 1, 0)
    high = min(size - 1, column + count - 1)
    num = boardrow[row]
    totscore += scoreHelpMe(low, high, num, color, count)*10 + scoreAnnoyOpponent(low, high, num, color, count)*9
    ##########
    low = max(row - count + 1, 0)
    high = min(size - 1, row + count - 1)
    num = boardcolumn[column]
    totscore += scoreHelpMe(low, high, num, color, count)*10 + scoreAnnoyOpponent(low, high, num, color, count)*9
    # #########1
    if row + column + 1 > size:
        low = max((column - (row + column - size) - count), 0)
        high = min((column - (row + column - size) + count - 2), size * 2 - (row + column + 2))
    else:
        low = max((column - count + 1), 0)
        high = min((column + count - 1), row + column)
    num = boarddiaright[(row + column + 1) - 1]
    totscore += scoreHelpMe(low, high, num, color, count)*10 + scoreAnnoyOpponent(low, high, num, color, count)*9
    ##########
    if column > row:
        low = max((row - count + 1), 0)
        high = min((row + count - 1), size - column + row - 1)
    else:
        low = max((column - count + 1), 0)
        high = min((column + count - 1), size - row + column - 1)
    num = boarddialeft[(column + size - row) - 1]
    totscore += scoreHelpMe(low, high, num, color, count)*10 + scoreAnnoyOpponent(low, high, num, color, count)*9
    return totscore


def scoreHelpMe(low, high, num, color, count):
    countmax = 0
    while low <= high - count + 1:
        #### checking if there is an unblocked 4 or 5
        j = 0
        counttimes = 0
        flag = 0
        num1 = num >> 2 * low
        while j < 6 and flag == 0:
            if (num1 & 3 == color):
                if j == 0 or j == 5:
                    flag = 2
                    counttimes = 0
                else:
                    counttimes += 1
            if num1 & 3 == color^1 and j != 5:
                flag = 1
                counttimes = 0
            j += 1
            num1 >>= 2
        if flag == 0 and counttimes >= 3:
            countmax = counttimes + 1
        #### checkinf how many in a row there are
        counttimes = 0
        i = 0
        num2 = num >> 2 * low
        while i<5 and flag != 1 and countmax<4:
            if num2 & 3 == color:
                counttimes += 1
            if num2 & 3 == color^1:
                flag = 1
                counttimes = 0
            i += 1
            num2 >>= 2
        if counttimes > countmax:
            countmax = counttimes
        low += 1
    if countmax ==5:
        if color == 2:
            return (1 << (countmax) * 4)
        else:
            return (1 << (countmax*4)) * (-1)
    if countmax >= 2:
        if color == 2:
            return (1 << ((countmax - 2)) * 3)
        else:
            return (1 << ((countmax - 2)) * 3)*(-1)
    return 0


def scoreAnnoyOpponent(low, high, num, color, count):
    countmax = 0
    while low <= high - count + 1:
        j = 0
        counttimes = 0
        flag = 0
        num1 = num >> 2 * low
        while j < 6 and flag == 0:
            if (num1 & 3 == color^1):
                if j == 0 or j == 5:
                    flag = 2
                    counttimes = 0
                else:
                    counttimes += 1
            if num1 & 3 == color and j != 5:
                flag = 1
                counttimes = 0
            j += 1
            num1 >>= 2
        if flag == 0 and counttimes >= 3:
            countmax = counttimes + 1
        i = 0
        counttimes = 0
        countmetimes = 0
        flag = 0
        num1 = num >> 2 * low
        while i < 5 and flag != 1 and countmax<4:
            if num1 & 3 == color^1:
                counttimes += 1
            if num1 & 3 == color:
                countmetimes += 1
            i += 1
            num1 >>= 2
        if countmetimes > 1:
            counttimes = 0
        if counttimes > countmax:
            countmax = counttimes
        low += 1
    if countmax >= 1:
        if color == 2:
            return (1 << ((countmax-1))*3)
        else:
            return (1 << ((countmax-1)*3))*(-1)
    return 0


def choose_best_places(count, boarddiaright, boarddialeft, boardrow, boardcolumn, size, color, boardpavailable):
    places = []
    count1 = 0
    for r in range (0, size):
        rowavailable = boardpavailable[r]
        while rowavailable != 0:
            place = 1
            c = 0
            while rowavailable & place == 0:
                place <<= 2
                c += 1
            rowavailable ^= place
            update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
            totscore = score(count, r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size, color)
            places.append((totscore,r,c))
            count1+=1
            update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
    places.sort()
    if color == 2:
        return places[(count1-10):]
    else:
        return places[:10]


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
    mask = 341
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


def gomokupvp(r, c, count, turn, boarddiaright, boarddialeft, boardrow, boardcolumn, size):
    color = 3-(turn & 1)
    update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
    win = checkwin(count, r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
    if win == 1:
        print "player 1 has won"
        return 1
    elif win == -1:
        print "player 2 has won"
        return -1
    return 0


def basic_mm_gomoku(count, color, boarddiaright, boarddialeft, boardrow, boardcolumn, boardpavailable, size, depth, remaining):
    bestrow = 0xdeadbeef
    bestcolumn = 0xdeadbeef
    best = -10000000000 if color == 2 else 10000000000
    places = choose_best_places(count, boarddiaright, boarddialeft, boardrow, boardcolumn, size, color, boardpavailable)
    # print "  " * depth, "begin d = ", depth, "color = ", color , "places before = ", places
    flag = 0
    i = 0
    while (i<len(places) and flag == 0):
        r = places[i][1]
        c = places[i][2]
        update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
        w = score(count, r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size, color)
        if w < (1<<20) and w > (1<<20)*-1:
            if remaining > 1 and depth<3:
                place = 1 << (2 * c)
                boardpavailable[r] ^= place
                # print "placeing color = ", color, "r, c = ",r, c
                w, row, column = basic_mm_gomoku(count, color^1, boarddiaright, boarddialeft, boardrow, boardcolumn, boardpavailable, size, depth+1, remaining-1)
                boardpavailable[r]^= place
        else:
            flag = 1
            #print "skiping sure win at color = ", color, "r, c = ",r, c
        update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
        if (color == 3 and w <= best) or (color == 2 and w >= best):
            best = w
            bestrow = r
            bestcolumn = c
        i += 1
    # print "  " * depth, "exit d =", depth, "color = ", color, "best = ", best, bestrow, bestcolumn, ", places after = ", places
    return best, bestrow, bestcolumn


def mm_vs_player_gomoku(count, boarddiaright, boarddialeft, boardrow, boardcolumn, boardpavailable, size, turn): # R is inputed as 0
    flag = 0
    remaining = size*size
    color = 3
    s, r, c = basic_mm_gomoku(count, color, boarddiaright, boarddialeft, boardrow, boardcolumn, boardpavailable, size,0, remaining)
    # print "computer places here: \n", "Row: ", r, "Column: ",c
    place = 1 << 2 * (c)
    boardpavailable[r] ^= place
    update(r, c, color, boarddiaright, boarddialeft, boardrow, boardcolumn, size) # Updating the boards.
    win = checkwin(count, r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
    # print "win p2 =", win
    if win == -1:
        print "The Computer Has Won"
    turn +=2
    remaining -= 1
    return win, r, c



class Board(GridLayout):

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.cols = 10
        self.rows = 10
        self.boardrow1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.boardcolumn1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.boarddiaright1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.boarddialeft1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.boardpavailable = [349525, 349525, 349525, 349525, 349525, 349525, 349525, 349525, 349525, 349525]
        self.buttons = [[], [], [], [], [], [], [], [], [], []]
        self.count = 5
        self.turn = 1
        self.win = 0
        self.remaining = 100
        for i in range (self.rows):
            for j in range (self.cols):
                button = MyButton(self, i, j)
                self.add_widget(button)
                self.buttons[i].append(button)


class MyButton(ButtonBehavior, Image):
    def __init__(self, board, r, c, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.source = 'C://Users/Tzur Lehavi/Desktop/images.png'
        self.bind(on_press=partial(callback, board, self, r, c))

def callback1(binstance, button, r, c, instance):
    if binstance.win == 0 and binstance.turn <= binstance.rows*binstance.rows:
        maskr = (1 << 2*(c))
        print binstance.boardrow1, binstance.boardrow1[r], maskr, r, c
        if binstance.boardrow1[r] & maskr*3 == maskr*2 or binstance.boardrow1[r] & maskr*3 == maskr*3:
            print "Try Again"
        else:
            button.source = 'C://Users/Tzur Lehavi/Desktop/BlackGo.jpg' if binstance.turn & 1 == 1 else 'C://Users/Tzur Lehavi/Desktop/WhiteGo.png'
            binstance.win = gomokupvp(r, c, binstance.count, binstance.turn, binstance.boarddiaright1, binstance.boarddialeft1,
                            binstance.boardrow1, binstance.boardcolumn1, binstance.rows)


def callback(binstance, button, r, c, instance):
    if binstance.win == 0 and binstance.turn <= binstance.rows*binstance.rows:
        maskr = (1 << 2*(c))
        if binstance.boardrow1[r] & maskr*3 == maskr*2 or binstance.boardrow1[r] & maskr*3 == maskr*3:
            print "Try Again"
        else:
            update(r, c, 2, binstance.boarddiaright1, binstance.boarddialeft1, binstance.boardrow1,
                   binstance.boardcolumn1, binstance.rows)
            binstance.win = checkwin(binstance.count, r, c, binstance.boarddiaright1, binstance.boarddialeft1,
                                     binstance.boardrow1, binstance.boardcolumn1, binstance.rows)
            binstance.boardpavailable[r] ^= 1 << 2 * c
            button.source = 'C://Users/Tzur Lehavi/Desktop/BlackGo1.jpg'
        if binstance.win == 0:
            binstance.win, r, c = mm_vs_player_gomoku(binstance.count, binstance.boarddiaright1, binstance.boarddialeft1, binstance.boardrow1, binstance.boardcolumn1, binstance.boardpavailable, binstance.rows, binstance.turn)
            binstance.buttons[r][c].source = 'C://Users/Tzur Lehavi/Desktop/WhiteGo1.jpg'
            print binstance.win
            binstance.turn += 1


class MyApp(App):

    def build(self):
        return Board()


if __name__ == '__main__':
    MyApp().run()
