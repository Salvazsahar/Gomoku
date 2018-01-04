from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from functools import partial
import math


global gomokupvp
def gomokupvp(r, c, count, turn, boarddiaright, boarddialeft, boardrow, boardcolumn, size):
    color = 3-(turn & 1)
    boardrow[r-1] += (1 << 2*(c-1))*color
    # Column
    boardcolumn[c - 1] += (1 << 2*(r - 1)) * color
    # Right Diagonal
    if r+c-1 > size:
        boarddiaright[(r+c-1) - 1] += (1 << 2*(c-(r+c-1-size)-1)) * color
    else:
        boarddiaright[(r+c-1)-1] += (1 << 2*(c-1)) * color
    # Left Diagonal
    if c+size-r > size:
        boarddialeft[(c+size-r) - 1] += (1 << 2*(r-1)) * color
    else:
        boarddialeft[(c+size-r)-1] += (1 << 2*(c-1)) * color
    # End Placement
    printboardrow(boardrow)
    print boarddialeft, "aaaaa"
    win = checkwin(count, r, c, boarddiaright, boarddialeft, boardrow, boardcolumn, size)
    if win == 1:
        print "player 1 has won"
    elif win == -1:
        print "player 2 has won"
    return win


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


def checkwin(count, row, column, boarddiaright, boarddialeft, boardrow, boardcolumn, size):
    mask = 85
    low = max(column - count, 0)
    high = min(size - 1, column + count - 2)
    num = boardrow[row - 1]
    while low <= high - count + 1:
        if (num >> 2*low) & mask*3 == mask*2:
            return 1
        elif (num >> 2 * low) & mask * 3 == mask * 3:
            return -1
        low += 1
    ##########
    low = max(row - count, 0)
    high = min(size - 1, row + count - 2)
    num = boardcolumn[column - 1]
    while low <= high - count + 1:
        if (num >> 2 * low) & mask * 3 == mask * 2:
            return 1
        elif (num >> 2 * low) & mask * 3 == mask * 3:
            return -1
        low += 1
    # #########1
    if row + column - 1 > size:
        low = max((column - (row + column - 1 - size) - count), 0)
        high = min((column - (row + column - 1 - size) + count-2), row - 1 - 1)
    else:
        low = max((column - count), 0)
        high = min((column + count-2), column - 1)
    num = boarddiaright[(row + column - 1) - 1]
    while low <= high - count + 1:
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
    while low <= high-count+1:
        if (num >> (2*low)) & (mask*3) == mask * 2:
            return 1
        elif (num >> (2 * low)) & (mask * 3) == mask * 3:
            return -1
        low += 1
    return 0


class Board(GridLayout, Image):

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.cols = 5
        self.rows = 5
        self.boardrow1 = [0, 0, 0, 0, 0]
        self.boardcolumn1 = [0, 0, 0, 0, 0]
        self.boarddiaright1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.boarddialeft1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.buttons = []
        self.count = 4
        self.turn = 1
        self.win = 0

        for i in range (self.rows):
            for j in range (self.cols):
                str1 = (str(i+1)+'-'+str(j+1))
                self.buttons.append(Button(text=str1))
                self.buttons[-1].bind(on_press=partial(callback, self, i+1, j+1))
                self.add_widget(self.buttons[-1])

def callback(binstance, r, c, instance):
    print "apple"
    print type(c)
    maskr = (1 << 2*(c-1))
    print binstance.boardrow1, binstance.boardrow1[r-1], maskr, r, c
    if binstance.boardrow1[r-1] & maskr*3 == maskr*2 or binstance.boardrow1[r-1] & maskr*3 == maskr*3:
        print "Try Again"
    else:
        win = gomokupvp(r, c, binstance.count, binstance.turn, binstance.boarddiaright1, binstance.boarddialeft1,
                        binstance.boardrow1, binstance.boardcolumn1, 5)
        print win
        binstance.turn += 1


    # Move the checking part of the function to outside the function itself in order for the "trying again" to be possible


class MyApp(App):

    def build(self):
        return Board()


if __name__ == '__main__':
    MyApp().run()

