# -*- coding: utf-8 -*-
__author__ = 'tunghoang'
import timeit
import numpy as np
from DnD import *
from math import *
import matplotlib.pyplot as plt
from random import randint, choice

class Road:

    # Initialisierung vom Weg-Objekt Konstruktur
    def __init__(self, map, start, end, roadID,startingRoomID,destinationID, *setCounter):
        self.fromID = startingRoomID
        self.toID = destinationID
        self.roadID = roadID
        self.start = start
        self.end = end
        self.road = []
        self.map = map
        self.roadCounter = []
        self.widthOfMap = np.shape(self.map)[0]
        self.heightOfMap = np.shape(self.map)[1]
        if setCounter:

            for el in setCounter: self.setCounter = el
            self.deadendCreating()
            self.deadend = True
            self.mid = None

        else:

            self.deadend = False
            self.setRoadONB()



    """ SEACHINGFUNCTION"""

    def mapCheck(self, node ,direction, distance):

    # direction  = (axis,direction)  y = 0, x = 1, positive = -1, negative = 1
    # bottom  = (0,1) , right  = (1,1), bottom  = (0,-1), bottom  = (1, -1)
        selected = [node[0],node[1]]

        try:
            
            selected[direction[0]] += distance * direction[1]
            if ((selected[0] >= 0) and (selected[1] >= 0)):     # y,x > 0
                return self.map[selected[0]][selected[1]]       
            else: return -1
        except (IndexError):
                return -1

    def lineCheck(self,node,direction,distance):

        selected = [node[0],node[1]]        #pointer
        result = []

        for i in range(distance):
            # trục của node += 1/-1
            selected[direction[0]] += direction[1]
            try:
                if ((selected[0] >= 0) and (selected[1] >= 0)):         # y,x > 0
                    result.append(self.map[selected[0]][selected[1]])
                else: result.append(-1)
            except (IndexError):
                result.append(-1)

        return result


    """ RANDOM OPTION """

    def obstacleAvoid(self,start,end,direction):

        axis = abs(direction[0] - 1)                
        side = 1                                    # negative = 1 , positive = -1 , default = negative
        if direction[0] == 1: rev = 0
        else: rev = 1
        # 0 = positive , 1 = negative , 2 = density
        selectedList = [[start[0],start[1]] , [start[0],start[1]], [start[0],start[1]]]

        endLoop = [True,True,True]
        result = [[],[]]

        selectedList[2][direction[0]] += direction[1]   #density + 1

        """ obstacle measurement """

        while (True in endLoop):

            # terms: 0: positive 1: negative, 2: density
            terms = [self.mapCheck(selectedList[0],direction,2),self.mapCheck(selectedList[1],direction,2),self.mapCheck(selectedList[2],direction,1)]

            if (terms[0] == 10):            # room = true
                result[0].append((selectedList[0][0],selectedList[0][1]))
                selectedList[0][axis] -= 1  # pos -= 1
            elif (terms[0] == -1):
                result[0].append(False)
                endLoop[0] = False
            else: endLoop[0] = False        # room = False stop

            if (terms[1] == 10 ):           # room = true
                result[1].append((selectedList[1][0],selectedList[1][1]))
                selectedList[1][axis] += 1  # neg += 1
            elif (terms[1] == -1):
                result[1].append(False)
                endLoop[1] = False          # room = False stop
            else: endLoop[1] = False

            if (terms[2] == 0): endLoop[2] = False
            else:selectedList[2][direction[0]] += direction[1]



        if  selectedList[2][direction[0]] + direction[1] <= end[direction[0]]:
            selectedList[2][direction[0]] += direction[1]   #density + 1


        """ Result optimizing """

        sTerms = [abs(selectedList[0][axis] - end[axis]),abs(selectedList[1][axis] - end[axis])]

        if False in result[0]:
            result.remove(result[0])        # pos = False
            selectedList.remove(selectedList[0])

        elif False in result[1]:          # pos = True
            result.remove(result[1])
            selectedList.remove(selectedList[1])
            side = -1
        elif sTerms[0] > sTerms[1]:      # pos = False
            result.remove(result[0])
            selectedList.remove(selectedList[0])

        else:                               # pos = True
            result.remove(result[1])
            selectedList.remove(selectedList[1])
            side = -1



        """ additional Margin """

        result[0].append((selectedList[0][0],selectedList[0][1]))


        if self.mapCheck(selectedList[0],(axis,side),1) == 0:    #margin +1 free
            selectedList[0][axis] += side
            result[0].append((selectedList[0][0],selectedList[0][1]))


        if ((self.mapCheck(selectedList[1],direction,1) == 0) and (selectedList[1][direction[0]] + direction[1] <= end[direction[0]])) :
            selectedList[1][direction[0]] += direction[1]



        """ mid determining """

        Act = False

        if start[rev] == end[rev]:
            if direction[0] == 0:   mid = [selectedList[1][0],selectedList[0][1]]       # mid = [density[0],rule[1]]
            else:                   mid = [selectedList[0][0],selectedList[1][1]]       # mid = [rule[0],density[1]]

        else:

            if direction[0] == 0:   selectedList[1] = (end[0],selectedList[0][1])       # density = [end[0],rule[1]]
            else:                   selectedList[1] = (selectedList[0][0],end[1])       # density = [rule[0],end[1]]
            Act = True




        """ created point """
        if Act:

            for i in range(abs(selectedList[0][direction[0]] - selectedList[1][direction[0]])):
                selectedList[0][direction[0]] += direction[1]
                result[0].append((selectedList[0][0],selectedList[0][1]))
            result.append(selectedList[1])

        else:

             # rule -> mid
            for i in range(abs(selectedList[0][direction[0]] - mid[direction[0]])):
                selectedList[0][direction[0]] += direction[1]
                result[0].append((selectedList[0][0],selectedList[0][1]))

            # rule -> mid
            for i in range(abs(mid[axis] - selectedList[1][axis])):
                mid[axis] -= side
                result[0].append((mid[0],mid[1]))



        return result

    def repair(self, node, destinationD):

        # pointer check True
        #destinationD = (axis,value)
        selected =[node[0],node[1]]

        while( self.mapCheck(selected,destinationD,1) == 10):
            selected[destinationD[0]] += destinationD[1]

        # margin + 2
        if (self.mapCheck(selected,destinationD,2) == 0):
            selected[destinationD[0]] += (destinationD[1] * 2 )
        # margin + 1
        elif (self.mapCheck(selected,destinationD,2) == 0):
            selected[destinationD[0]] += (destinationD[1] * 1 )

        else: return 0

        return selected

    def setDirection(self):

        coordinate = [self.start[0] - self.end[0], self.start[1] - self.end[1]]
        direction = [[0,0],[1,0]]


        if coordinate[0] < 0: direction[0][1] = 1           # start(y) - end(y) < 0 => direction  = negative
        elif coordinate[0] > 0: direction[0][1] = -1        # start(y) - end(y) > 0 => direction  = positive
        else:
            direction[0][0] = 1                             # start(y) - end(y) == 0 => same y
            if coordinate[1] < 0: direction[0][1] = 1
            if coordinate[1] > 0: direction[0][1] = -1

        if coordinate[1] < 0: direction[1][1] = 1           # start(x) - end(x) < 0 => direction  = negative
        elif coordinate[1] > 0: direction[1][1] = -1        # start(x) - end(x) < 0 => direction  = positve
        else:
            direction[1][1] = 0
            if coordinate[0] < 0: direction[1][0] = 1
            if coordinate[0] > 0: direction[1][0] = -1

        random = randint(0,1)
        if random == 1: direction[::-1]

        return direction

    def Road(self):
        #time debug

        direction = self.setDirection()

        # set mid
        if (direction[0][0] == 0):
             mid = [self.end[0],self.start[1]]
        else:   mid = [self.start[0],self.end[1]]

        if (self.mapCheck(mid,direction[0],0) == 10):
            mid = self.repair(mid,direction[1])

        start = list(self.start)
        first = self.lineCheck(start,direction[0],abs(start[direction[0][0]] - mid[direction[0][0]]))
        self.road.append(self.start)
        i = 0


        starttime = timeit.default_timer()

        while (i < len(first)):
            if first[i] == 0:
                start[direction[0][0]] += direction[0][1]
                self.road.append((start[0],start[1]))
                i += 1
            else:
                # tạo m
                start[direction[0][0]] -= direction[0][1]
                self.road.remove(self.road[len(self.road)-1])

                p = self.obstacleAvoid(start,(mid[0],mid[1]),direction[0])
                self.road.extend(p[0])

                a = p[0][len(p[0])-1]
                if (a[direction[0][0]] - self.end[direction[0][0]]) != 0:
                    i = a[direction[0][0]]
                    start = [a[0],a[1]]
                else: break



        nd = self.lineCheck(mid,direction[1],abs(mid[direction[1][0]] - self.end[direction[1][0]]))

        starttime = timeit.default_timer()

        self.road.append((mid[0],mid[1]))
        n = 0
        while (n < len(nd)):
            if nd[n] == 0:
                mid[direction[1][0]] += direction[1][1]
                self.road.append((mid[0],mid[1]))
                n += 1
            else:
                mid[direction[1][0]] -= direction[1][1]
                self.road.remove(self.road[len(self.road)-1])

                p = self.obstacleAvoid(mid,self.end,direction[1])
                self.road.extend(p[0])
                a = p[0][len(p[0])-1]
                if (a[direction[1][0]] - self.end[direction[1][0]]) != 0:
                    n = a[direction[1][0]]
                    mid = [a[0],a[1]]
                else: break

        return  set(self.road)


    """GETFUNCTION"""


    def getRoad(self):
        return self.road

    def getMid(self):
        return self.mid

    def getLimit(self):
        return self.roadCounter

    def getFromID(self):
        return self.fromID

    def getToID(self):
        return self.toID

    def getDeadEnd(self):
        return self.deadend

    def getRoadID(self):
        return self.roadID

    """NEIGHBOR OPTION"""

    def setDirectionONB(self):

        if ((self.mapCheck(self.start,(0,1),1) == 10) or (self.mapCheck(self.start,(0,-1),1) == 10)): return ((0,1),(0,-1))
        else: return ((1,1),(1,-1))


    def setMidPointONB(self,direction):

        fl = floor(abs(self.start[direction[0][0]]- self.end[direction[0][0]])/2)
        ce = ceil(abs(self.start[direction[0][0]]- self.end[direction[0][0]])/2)
        midAxis = min(self.start[direction[0][0]], self.end[direction[0][0]]) + choice((fl,ce))

        if direction[0][0] == 0:
            result = [(midAxis,self.start[1]),(midAxis,self.end[1])]
            self.mid = result
            return result

        else:
            result =[(self.start[0],midAxis),(self.end[0],midAxis)]
            self.mid = result
            return result

    def setRoadONB(self):

        keys = [self.start]

        direction = self.setDirectionONB()
        midList = self.setMidPointONB(direction)
       
        keys.extend(midList)
        keys.append(self.end)

        for index in range(len(keys)-1):

            edge,limit = self.edgeCreating(keys[index],keys[index + 1])
            self.road.extend(edge)
            self.roadCounter.append(limit)

        self.road.append(self.end)


        return self.road

    def edgeCreating(self,start,end):

        if ((start[0] - end[0]) == 0): mainAxis = 1
        else: mainAxis = 0

        if start[mainAxis] < end[mainAxis]: value = 1
        else: value =  -1

        stack = []
        pointer = [start[0],start[1]]
        counter = 0

        while(pointer[mainAxis] != end[mainAxis]):
            stack.append((pointer[0],pointer[1]))
            pointer[mainAxis] += value
            counter += 1

        return stack, counter

    """DEAD END OPTION"""

    def midAxis(self):

        condition = [self.start[0] - self.end[0],self.start[1] - self.end[1]]
        self.keys =  []

        if condition[0] == 0:

            if condition[1] < 0: self.keys.append((1,1))
            else: self.keys.append((1,-1))
            self.keys.append((0,1))
            self.keys.append((0,-1))

        else:
            if condition[0] < 0: self.keys.append((0,1))
            else: self.keys.append((0,-1))
            self.keys.append((1,1))
            self.keys.append((1,-1))

        return self.keys

    def deadendCreating(self ):


        direction = self.midAxis()

        mAxis, neg, pos = direction[0], direction[1],direction[2]

        mLimit,negLimit, posLimit = self.setCounter[1],self.setCounter[0],self.setCounter[2]

        midSet = (self.start,self.end)
        #random m1, m2
        sel = choice(midSet)
        keys = [sel]

        index = midSet.index(sel)

        if index == 0:  selDirection = [mAxis[0], mAxis[1] * - 1]
        else:           selDirection = mAxis

        searchLine = self.lineCheck(sel,selDirection,mLimit-1)

        selected =[sel[0],sel[1]]
        for element in searchLine:

            if element < 0:
                selected[selDirection[0]] -= selDirection[1]
                break
            else:
                selected[selDirection[0]] += selDirection[1]


        keys.append((selected[0],selected[1]))
        nextBuild = choice((True,False))

        if nextBuild:

            mainAxis = choice((neg, pos))

            if mainAxis == neg: mainLimit =  negLimit - 1
            else: mainLimit = posLimit - 1

            searchLine = self.lineCheck(selected,mainAxis,mainLimit)

            for element in searchLine:
                if element != 0:
                    selected[mainAxis[0]] -= mainAxis[1]
                    break
                else:
                    selected[mainAxis[0]] += mainAxis[1]

            keys.append((selected[0],selected[1]))


        for keyIdx in range(len(keys)-1):

            edge, counter = self.edgeCreating(keys[keyIdx],keys[keyIdx + 1])
            self.roadCounter.append(counter)
            self.road.extend(edge)

        return self.road


if __name__ == '__main__':

    test = np.zeros((50,50), dtype = np.int)

    test[3:7,0:3] = 10
    test[8:15,16:22] = 10
    test[15:20,7:10] = 10
    test1 = (4, 9)
    test2 = (9, 9)
    test3 = (7,2)
    test4 = (14,9)


    counter = [6, 5, 6]

    #def __init__(self, map, start, end, roadID,startingRoomID,destinationID,*randomRoad):
    a = Road(test,test1,test2,1,1,2,counter)
    selection = a.getRoad()
    print(selection)

    for el in selection:
        test[el[0]][el[1]] = 4


    arr = test
    plt.imshow(arr, interpolation='nearest',cmap=plt.cm.gray)
    plt.show()
