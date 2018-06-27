__author__ = 'tunghoang'
import numpy as np
#from  DnD_0054 import Dungeon
from math import *
import matplotlib.pyplot as plt
from random import randint, choice
"""
Version 0.060
"""

class Road:
    map = []                # DnD map
    field = []              # enthält alle Knoten, die keine Raum sind
    graph = {}              # Liste die Knoten, die untereinander adjazent sind
    costList = {}
    road = []               # alle Knoten vom endliche Weg
    widthOfMap = 0
    heightOfMap = 0


    # Initialisierung vom Weg-Objekt Konstruktur
    def __init__(self, map,):
        self.map = map

        self.widthOfMap = np.shape(self.map)[0]
        self.heightOfMap = np.shape(self.map)[1]
        self.mapScanner()
        #self.pfad_breitensuche()


    # diese Methode überprüft alle Knoten in der Karte und dann:
    # Field von den Knoten, auf den der Weg aufbaut werden kann und auf self.field speichert
    # Graph G wird erzeugt, der enthält die Verbindung zwischen Knoten miteinander
    def mapScanner(self):


        for row in range(self.heightOfMap):
            for column in range(self.widthOfMap):

                if self.map[row][column] == 0 or self.map[row][column] == 20:   #map[y_pos][x_pos] = 0 bedeutet, dass diese Knote frei ist
                    self.field.append((row,column))                             #y_pos und x_pos werden verbunden als string mit der Form 'y_pos + x_pos'


        # self.graph erzeugen
        for key in self.field:
            right =     (key[0],        key[1] + 1)                     # recht, link , unter und ober Knoten werden erzeugt und
            bottom =    (key[0] + 1,    key[1])                         # wird überprüft, ob die frei sind oder nicht
            left =      (key[0],        key[1] - 1)
            top =       (key[0] - 1,    key[1])


            #  Knoten auf self.graph einfügen
            if (right in self.field):
                self.graph.setdefault(key, []).append(right)
                self.costList.setdefault(right )
                self.costList[right] = 1

            if (bottom in self.field):
                self.graph.setdefault(key, []).append(bottom)
                self.costList.setdefault(bottom)
                self.costList[bottom] = 1

            if (left in self.field):
                self.graph.setdefault(key, []).append(left)
                self.costList.setdefault(left)
                self.costList[left] = 1

            if (top in self.field):
                self.graph.setdefault(key, []).append(top)
                self.costList.setdefault(top)
                self.costList[top] = 1


        return self.graph

    #Breadth-First-Search implementieren mit startNode und endNode
    def pfad_breitensuche(self,startNode,endNode):
        self.startNode = startNode[::-1]
        self.endNode = endNode[::-1]

        check1 = self.graph.__contains__(self.startNode)  #ueberprueft, ob Start-Knoten in Graphen ist.
        check2 = self.graph.__contains__(self.endNode)    #ueberprueft, ob End-Knoten in Graphen ist.

        if(check1 & check2):
            queue = [[self.startNode]]

            while(len(queue) != 0):

                pfad = queue.pop(0)
                aktueller_knoten = pfad[len(pfad) - 1]
                naechste_knoten = set(self.graph[aktueller_knoten]) - set(pfad)

                for knoten in sorted(naechste_knoten):

                    queue.append(pfad + [knoten])
                    if (knoten == self.endNode):

                        self.road.append(pfad + [knoten])
                        queue = []
                        break

        temp = []

        return self.road

    def nearestPoint(self,node,start,end):
        axis = 1
        x = node[1]
        y = node[0]
        # top bottom left right
        check =[False ,False ,False ,False]

        while(axis < 100):
            # top bottom left right
            candidates = [(y - axis, x), (y + axis, x),(y,x - axis),(y,x + axis)]

            for r in range(0,len(candidates)):
                if candidates[r] in self.field:
                    check[r] = True

            # alle nicht False sind
            if (True in check):
                for c in range(len(check)):
                    if (check[c] == True) and (candidates[c] != start)  and  (candidates[c] != end):
                        if ((candidates[c][0] < start[0] or candidates[c][0] > end[0]) and (c == 2 or c == 3)):
                            return candidates[c]
                        return candidates[c]

            axis+=1


    def roadCreating(self,start,end,direction,depth):
        global count

        if end == start: return
        elif self.nodeCheck(start,end) == True: return

        d = direction
        if (end[0] - start[0] <= 0) :
            if (d == 0):        y_mid = floor(abs(end[0] - start[0])/2) + end[0]
            elif(d == 1):       y_mid = ceil(abs(end[0] - start[0])/2) + end[0]
        else:
            if (d == 0):        y_mid = floor(abs(end[0] - start[0])/2) + start[0]
            elif(d == 1):       y_mid = ceil(abs(end[0] - start[0])/2) + start[0]


        if (end[1] - start[1] <= 0) :
            if (d == 0):        x_mid = floor(abs(end[1] - start[1])/2) + end[1]
            elif(d == 1):       x_mid = ceil(abs(end[1] - start[1])/2) + end[1]
        else:
            if (d == 0):        x_mid = floor(abs(end[1] - start[1])/2) + start[1]
            elif(d == 1):       x_mid = ceil(abs(end[1] - start[1])/2) + start[1]


        mid = (y_mid,x_mid)

        depth += 1
        if (mid not in self.field):

            mid = self.nearestPoint((y_mid,x_mid),start,end)




        self.roadCreating(start,mid,0,depth)
        self.roadCreating(mid,end,1,depth)
        self.road.append(mid)


        return mid

    def nodeCheck(self,root,next):

        list = []

        for y in range(root[0]-1, root[0]+2):
            for x in range(root[1]-1, root[1]+2):
                list.append((y,x))


        if (next in list):

            return True

        return False


    def fillRoad(self,start,end):
        for r in self.map:
            for node in self.road:
                self.map[node[0]][node[1]] = 2.5
        self.map[start[0]][start[1]] = 9
        self.map[end[0]][end[1]] = 6







