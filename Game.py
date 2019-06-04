from tkinter import *
import random
from Box import Box
from time import sleep
import copy


'''
*** Rules for John Conway's Game of Life ***

For a space that is 'populated':
    Each cell with one or no neighbors dies, as if by solitude.
    Each cell with four or more neighbors dies, as if by overpopulation.
    Each cell with two or three neighbors survives.
For a space that is 'empty' or 'unpopulated'
    Each cell with three neighbors becomes populated.
'''

boxes = []  # List of all Boxes
nextBoxes = []  # List of next tick boxes
canvas = None
tickTime = (1 / 60)  # 1 / fps
cWidth = 500
cHeight = 500
boxSize = 25  # Each box is boxSize x boxSize in pixels
wBoxes = cWidth / boxSize
hBoxes = cHeight / boxSize

# Function used to setup first on boxes


def setFirstBoxes():
    global boxes

    for box in boxes:
        # Random starting boxes
        rand = random.randint(0, 9)

        if(rand < 3):
            box.on = True
            canvas.itemconfig(box.num, fill="yellow")

        # Turns on a middle row of boxes
        # if(box.row == 10 and box.col >= 5 and box.col < 15):
        #     box.on = True
        #     canvas.itemconfig(box.num, fill="yellow")

# Returns the number of neighbors that are

def numOfNeighors(box):
    numOfNeighors = 0
    for n in box.neighbors:
        box = findBoxByCord(n[0], n[1])

        if(box.on):
            numOfNeighors += 1

    return numOfNeighors


# Function called on each tick and contains main Game of Life Logic


def onTick():
    global boxes
    global nextBoxes

    for temp in boxes:

        box = copy.copy(temp)
        neighborsOn = numOfNeighors(box)

        if(box.on):
            # print(box)
            # print(neighborsOn)
            # print()
            if(neighborsOn == 1 or neighborsOn == 0):
                box.on = False
                canvas.itemconfig(box.num, fill="gray")
            elif(neighborsOn >= 4):
                box.on = False
                canvas.itemconfig(box.num, fill="gray")
            # elif(neighborsOn == 2 or neighborsOn == 3):
            #     # print("Survives")
        else:
            if(neighborsOn == 3):
                box.on = True
                canvas.itemconfig(box.num, fill="yellow")

        nextBoxes.append(box)
    # print(len(nextBoxes))
    boxes = nextBoxes
    nextBoxes = []

# Adds neighbors to each box


def fillNeighbors():
    for box in boxes:
        temp = []
        row = box.row
        col = box.col

        if(row - 1 >= 0):
            temp.append((row - 1, col))
        if(row + 1 < hBoxes):
            temp.append((row + 1, col))
        if(col - 1 >= 0):
            temp.append((row, col - 1))
        if(col + 1 < wBoxes):
            temp.append((row, col + 1))

        if(row - 1 >= 0 and col - 1 >= 0):
            temp.append((row - 1, col - 1))
        if(row - 1 >= 0 and col + 1 < wBoxes):
            temp.append((row - 1, col + 1))
        if(row + 1 < hBoxes and col - 1 >= 0):
            temp.append((row + 1, col - 1))
        if(row + 1 < hBoxes and col + 1 < wBoxes):
            temp.append((row + 1, col + 1))

        box.neighbors = temp

# Finds a box by the number given


def findBoxByNum(num):
    if(num < 1 or num > ((cWidth / boxSize) * (cWidth / boxSize))):
        return None

    for i in boxes:
        if(i.num == num):
            return i

    return None

# Finds a box by the coordinates given


def findBoxByCord(row, col):
    if(row < 0 or row >= (cHeight / boxSize) or col < 0 or col >= (cWidth / boxSize)):
        return None

    for i in boxes:
        if(i.row == row and i.col == col):
            return i

    return None

# Function called whenever a box is pressed


def boxClicked(event):

    num = canvas.find_withtag(CURRENT)[0]
    # print(num)
    box = findBoxByNum(num)
    if(box is not None):
        # box.printNeighbors()
        box.on = True
        canvas.itemconfig(CURRENT, fill="yellow")

# Function that sets up the whole program

def setupWindow():
    global boxes
    global canvas

    win = Tk()
    win.title = "John Conway's Game of Life"

    canvas = Canvas(win, width=cWidth, height=cHeight)
    canvas.pack()

    for row in range(0, int(cHeight / boxSize)):
        for col in range(0, int(cWidth / boxSize)):
            temp = canvas.create_rectangle(
                row * boxSize, col * boxSize, (row * boxSize) + boxSize, (col * boxSize) + boxSize, fill="gray", tag="box")
            boxes.append(Box(temp, col, row))

    canvas.tag_bind("box", "<Button-1>", boxClicked)

    fillNeighbors()

    setFirstBoxes()

    # box = findBoxByCord(10,10)

    # print("NumOfNeigh = " + str(numOfNeighors(box)))
    # # print(box.on)

    # # onTick()

    # box = findBoxByCord(10,10)

    # print("NumOfNeigh = " + str(numOfNeighors(box)))
    # print(box.on)

    # win.mainloop()

    while True:
        win.update_idletasks()
        win.update()
        onTick()
        sleep(tickTime)


if __name__ == "__main__":
    setupWindow()
