from random import randint


def printboard(num, size):
    for i in range(size):
        for j in range(size):
            a = num & 3
            if a == 3:
                print "o",
            elif a == 2:
                print "x",
            else:
                print ".",
            num >>= 2
        print


def buildboard(size):
    num = 0
    for i in range(size*size):
        x = int(raw_input("Enter what should be in this place: "))
        place = 1 << 2*i
        num += x*place
    print num
    return num


def buildboardrnd(size):
    num = 0
    list1 = [0,2,3]
    for i in range(size * size):
        x = randint(0,2)
        x = list1[x]
        place = 1 << 2 * i
        num += x * place
    print num
    return num


def checkwin(board1, color, list1, size):
    i = 1
    for mask in list1:
        if board1 & mask*3 == mask*color:
            return 1
        board1 >>= 2


printboard(buildboardrnd(5),5)