# -*- coding: utf-8 -*-
__author__ = 'tunghoang'

import numpy as np
#from DnD0060 import *
from math import *
import matplotlib.pyplot as plt
from random import randint, choice

class Road:

    # Initialisierung vom Weg-Objekt Konstruktur
    def __init__(self, map, start, end, roadID,startingRoomID,destinationID, *random):
        self.fromID = startingRoomID    
        self.toID = destinationID       
        self.roadID = roadID            
        self.start = start              
        self.end = end                  
        self.road = []                  
        self.map = map
        self.widthOfMap = np.shape(self.map)[0]
        self.heightOfMap = np.shape(self.map)[1]
        if random:        
            self.setRoadONB()
        else:           
            self.setRoadONB()
  
    def mapCheck(self, node ,direction, distance):
    # direction  = (axis,direction)  y = 0, x = 1, positive = -1, negative = 1
    # bottom  = (0,1) , right  = (1,1), bottom  = (0,-1), bottom  = (1, -1)
        selected = [node[0],node[1]]
        
        try:
            
            selected[direction[0]] += distance * direction[1]
            if ((selected[0] >= 0) and (selected[1] >= 0)):     # y,x > 0
                return self.map[selected[0]][selected[1]]       # giá trị của tọa độ trên map
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
                else: result.append(False)
            except (IndexError):
                result.append(False)

        return result



    def obstacleAvoid(self,start,end,direction):

        axis = abs(direction[0] - 1)               
        side = 1                                    
        if direction[0] == 1: rev = 0               
        else: rev = 1
        # 0 = positive , 1 = negative , 2 = density
        selectedList = [[start[0],start[1]] , [start[0],start[1]], [start[0],start[1]]]

        endLoop = [True,True,True]                  
        result = [[],[]]                            

        selectedList[2][direction[0]] += direction[1]   #density + 1

        
        while (True in endLoop):
           
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

        result[0].append((selectedList[0][0],selectedList[0][1]))

        if self.mapCheck(selectedList[0],(axis,side),1) == 0:    #margin +1 free
            selectedList[0][axis] += side
            result[0].append((selectedList[0][0],selectedList[0][1]))

        if ((self.mapCheck(selectedList[1],direction,1) == 0) and (selectedList[1][direction[0]] + direction[1] <= end[direction[0]])) :
            selectedList[1][direction[0]] += direction[1]

       
        """ end compare """

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

            # mid -> end
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

        #print(mid)
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

    def getRoad(self):
        return self.road
    
    def setDirectionONB(self):

        if ((self.mapCheck(self.start,(0,1),1) == 10) or (self.mapCheck(self.start,(0,-1),1) == 10)): return ((0,1),(0,-1))
        else: return ((1,1),(1,-1))


    def setMidPointONB(self,direction):

        fl = floor(abs(self.start[direction[0][0]]- self.end[direction[0][0]])/2)
        ce = ceil(abs(self.start[direction[0][0]]- self.end[direction[0][0]])/2)
        midAxis = min(self.start[direction[0][0]], self.end[direction[0][0]]) + choice((fl,ce))

        if direction[0][0] == 0:
            result = [(midAxis,self.start[1]),(midAxis,self.end[1])]
            return result

        else:
            result =[(self.start[0],midAxis),(self.end[0],midAxis)]
            return result

    def setRoadONB(self):

        keys = [self.start]

        direction = self.setDirectionONB()
        midList = self.setMidPointONB(direction)


        keys.extend(midList)
        keys.append(self.end)

        for index in range(len(keys)-1):

            edge = self.edgeCreating(keys[index],keys[index + 1])
            self.road.extend(edge)

        self.road.append(self.end)


        return self.road

    def edgeCreating(self,start,end):

        if ((start[0] - end[0]) == 0): mainAxis = 1
        else: mainAxis = 0

        if start[mainAxis] < end[mainAxis]: value = 1
        else: value =  -1

        stack = []
        pointer = [start[0],start[1]]


        while(pointer[mainAxis] != end[mainAxis]):
            stack.append((pointer[0],pointer[1]))
            pointer[mainAxis] += value

        return stack
    
    
    

