__author__ = 'tunghoang'
from random import randint
import numpy as np
import matplotlib.pyplot as plt
from Road import Road

class Dungeon:
    dMap =[]
    roomField =[]
    percentage = 50
    widthOfMap = 0
    heightOfMap = 0
    roads =[]

    # Initialisierung vom Dungeon
    def __init__(self,width,height,percentage):

        self.percentage = percentage
        self.widthOfMap = width
        self.heightOfMap = height
        temp = np.zeros((self.widthOfMap,self.heightOfMap), dtype=np.int)
        self.dMap = temp

    # Initialisierung vom Raum
    def roomInitializing(self,x_pos,y_pos, width, height, index):
        y_pos -= 1
        x_pos -= 1

        self.dMap[y_pos:y_pos + height, x_pos:x_pos+ width] = index
        for row in range(y_pos, y_pos + height ):
            for column in range(x_pos,x_pos+ width):
                self.roomField.append([row,column])


    # Position vom Raum überprüfen
    def positionCheck(self, x_pos, y_pos, width, height, distance):

        #Bedingung: wenn ein Raum außer Map
        if (x_pos + width > self.widthOfMap - 1   or y_pos + height > self.heightOfMap - 1 ):
            return False

        if ([x_pos, y_pos] in self.roomField):
            return False

        #Bedingung: Abstand zwischen 2 Räume
        top = y_pos
        bottom = y_pos + height
        left = x_pos
        right = x_pos + width

        # abstand checking

        maxDistance = distance
        if (distance > top and top <= maxDistance): maxDistance = top
        if (distance > left and left <= maxDistance ):  maxDistance = left
        if (distance > self.heightOfMap - 1 - bottom and  self.heightOfMap - bottom <= maxDistance ):  maxDistance = self.heightOfMap - 1  - bottom
        if (distance > self.widthOfMap - 1 -  right and  self.widthOfMap - right <= maxDistance ):  maxDistance = self.widthOfMap - 1 - right

        if (maxDistance < 0) : maxDistance = 0

        while(top < bottom):

            if    ([top - maxDistance, left]        in self.roomField       #top field checking
                or [bottom + maxDistance, left]     in self.roomField       #bottom field checking
                or [top, left - maxDistance]        in self.roomField       #left field
                or [top, right + maxDistance]       in self.roomField ):    #right field

                return False
            if (top < bottom):  top += 1
            if (left < right):  left += 1

        return True


    # mehrere Räume erstellen
    def multiRoom(self,numberOfRoom,maxW,maxH,distance):
        maxround = 100
        count = numberOfRoom

        while(count != 0 ):

            x_pos, y_pos = randint(0,self.widthOfMap) , randint(0,self.heightOfMap)
            wOfInstance, hOfInstance = randint(1,maxW) , randint(1,maxH)

            if (self.positionCheck(x_pos, y_pos, wOfInstance, hOfInstance,distance) == True):
                self.roomInitializing(x_pos,y_pos,wOfInstance,hOfInstance,count)
                count -= 1
            elif (maxround == 0):
                break

    # Weg erstellen
    def roadCreating(self,start,end):
        road = Road(self.dMap,start,end)
        road.fillRoad(self.dMap)
        self.roads.append(road)

    # Dungeon zurückgeben
    def returnArray(self):
        return self.dMap


if __name__ == '__main__':
    test = Dungeon(20,20,50)
    #test.multiRoom(2,5,5,1)
    test.roomInitializing(2,2,3,4,1)
    test.roomInitializing(13,7,3,2,4)
    test.roadCreating((4,1),(14,5))

    arr = test.returnArray()
    plt.imshow(arr,interpolation='nearest',cmap=plt.cm.gray)
    plt.show()

