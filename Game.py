from tkinter import *
import random
from Box import Box
from time import sleep
import copy

boxes = []
nextBoxes = []
onBoxes = []
canvas = None
tickTime = (1 / 1)  # 1 / fps
cWidth = 500
cHeight = 500
boxSize = 25


def setFirstBoxes():
    global boxes, onBoxes

    for box in boxes:
        # rand = random.randint(0,9)

        # if(rand < 1):
        #     box.on = True
        #     onBoxes.append(box)
        #     canvas.itemconfig(box.num, fill="yellow")

        if(box.row == 10 and box.col >= 5 and box.col < 15):
            box.on = True
            onBoxes.append(box)
            canvas.itemconfig(box.num, fill="yellow")


'''
For a space that is 'populated':
    Each cell with one or no neighbors dies, as if by solitude.
    Each cell with four or more neighbors dies, as if by overpopulation.
    Each cell with two or three neighbors survives.
For a space that is 'empty' or 'unpopulated'
    Each cell with three neighbors becomes populated.
'''


def onTick():
    global boxes
    global onBoxes
    global nextBoxes

    print(len(onBoxes))

    for temp in boxes:
        neighborsOn = 0
        box = copy.copy(temp)

        print(len(box.neighbors))
        for n in box.neighbors:

            if(n in onBoxes):
                neighborsOn += 1

        if(box.on):
            # print(box)
            # print(neighborsOn)
            # print()
            if(neighborsOn == 1 or neighborsOn == 0):
                box.on = False
                onBoxes.remove(box)
                canvas.itemconfig(box.num, fill="gray")
            elif(neighborsOn >= 4):
                box.on = False
                onBoxes.remove(box)
                canvas.itemconfig(box.num, fill="gray")
        else:
            if(neighborsOn == 3):
                box.on = True
                onBoxes.append(box)
                canvas.itemconfig(box.num, fill="yellow")

        nextBoxes.append(box)
    print(len(nextBoxes))
    boxes = nextBoxes
    nextBoxes = []


def fillNeighbors():
    for box in boxes:
        temp = []
        row = box.row
        col = box.col

        temp.append(findBoxByCord(row - 1, col))  # Up
        temp.append(findBoxByCord(row + 1, col))  # Down
        temp.append(findBoxByCord(row, col - 1))  # Left
        temp.append(findBoxByCord(row, col + 1))  # Right

        temp.append(findBoxByCord(row - 1, col-1))  # UpLeft
        temp.append(findBoxByCord(row - 1, col+1))  # UpRight
        temp.append(findBoxByCord(row + 1, col-1))  # DownLeft
        temp.append(findBoxByCord(row + 1, col+1))  # DownRight

        for item in temp:
            if(item is not None):
                box.neighbors.append(item)


def findBox(num):
    if(num < 1 or num > ((cWidth / boxSize) * (cWidth / boxSize))):
        return None

    for i in boxes:
        if(i.num == num):
            return i

    return None


def findBoxByCord(row, col):
    if(row < 0 or row >= (cHeight / boxSize) or col < 0 or col >= (cWidth / boxSize)):
        return None

    for i in boxes:
        if(i.row == row and i.col == col):
            return i

    return None


def boxClicked(event):
    global onBoxes

    num = canvas.find_withtag(CURRENT)[0]
    print(num)
    box = findBox(num)
    if(box is not None):
        box.printNeighbors()
        box.on = True
        canvas.itemconfig(CURRENT, fill="yellow")

        if(box not in onBoxes):
            onBoxes.append(box)


def clearBoxes():
    canvas.delete("all")


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

    while True:
        win.update_idletasks()
        win.update()
        onTick()
        sleep(tickTime)


if __name__ == "__main__":
    setupWindow()
