__author__ = 'tunghoang'
import numpy as np
#from  DnD import Dungeon
"""
temp = np.zeros((10,10), dtype=np.int)
temp[1:3, 1:3] = 1
temp[1:3, 1:3] = 1
"""

class Road:
    map = []                # DnD map
    field = []              # enthält alle Knoten, die keine Raum sind
    graph = {}              # Liste die Knoten, die untereinander adjazent sind
    road = []               # alle Knoten vom endliche Weg
    widthOfMap = 0
    heightOfMap = 0

    # Initialisierung vom Weg-Objekt Konstruktur
    def __init__(self, map, startNode, endNode):
        self.map = map
        self.startNode = startNode[::-1]
        self.endNode = endNode[::-1]
        self.widthOfMap = np.shape(self.map)[0]
        self.heightOfMap = np.shape(self.map)[1]
        self.mapScanner()
        self.pfad_breitensuche()


    # diese Methode überprüft alle Knoten in der Karte und dann:
    # Field von den Knoten, auf den der Weg aufbaut werden kann und auf self.field speichert
    # Graph G wird erzeugt, der enthält die Verbindung zwischen Knoten miteinander
    def mapScanner(self):


        for row in range(self.heightOfMap):
            for column in range(self.widthOfMap):

                if self.map[row][column] == 0:                           #map[y_pos][x_pos] = 0 bedeutet, dass diese Knote frei ist
                    self.field.append((row,column))                      #y_pos und x_pos werden verbunden als string mit der Form 'y_pos + x_pos'


        # self.graph erzeugen
        for key in self.field:
            right =     (key[0],        key[1] + 1)                     # recht, link , unter und ober Knoten werden erzeugt und
            bottom =    (key[0] + 1,    key[1])                         # wird überprüft, ob die frei sind oder nicht
            left =      (key[0],        key[1] - 1)
            top =       (key[0] - 1,    key[1])


            #  Knoten auf self.graph einfügen
            if (right in self.field):     self.graph.setdefault(key, []).append(right)
            if (bottom in self.field):    self.graph.setdefault(key, []).append(bottom)
            if (left in self.field):      self.graph.setdefault(key, []).append(left)
            if (top in self.field):       self.graph.setdefault(key, []).append(top)

        return self.graph

    #Breadth-First-Search implementieren mit startNode und endNode
    def pfad_breitensuche(self):

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
        if (len(self.map) != 0):
            for node in self.road[0]:
                temp.append(node)
            self.road = temp
        return self.road


    # Weg auf der Karte einfügen
    def fillRoad(self, map):
        for node in self.road:
            map[node[0]][node[1]] = 15
        return map

    def showMap(self):
        for row in self.map:
            print (row)
"""
if __name__ == '__main__':
    test = Dungeon(20,20,50)
    #test.multiRoom(2,5,5,1)
    test.roomInitializing(2,2,3,4,1)
    test.roomInitializing(15,8,3,2,4)
    test2 = Road(test.returnArray(),(4,1),(14,5))

    print(test2.fillRoad(test.returnArray()))

"""