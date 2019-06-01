from tkinter import *

class Box:
    
    def __init__(self, num, row, col):
        self.row = row
        self.col = col
        self.on = False
        self.num = num
        self.neighbors = []

    def __str__(self):
        return "#" + str(self.num) + " Row: " + str(self.row) + " Col: " + str(self.col) + " On: " + str(self.on)

    def __eq__(self, other):
        if(isinstance(other, Box)):
            if(other.row == self.row and other.col == self.col):
                return True

        return False

    def printNeighbors(self):
        for n in self.neighbors:
            print(n)

        print()
