__author__ = 'tunghoang'
from random import randint, choice
from RoadVer056 import *
from math import *
import numpy as np
import matplotlib.pyplot as plt
#from Road import Road
"""
Dnd Generator version 0.060
"""
class Room:
    border ={}
    roomID = 0
    fieldID = 0
    field = ((0,0),(0,0))
    safety = 0
    shape = [0,0]    #(height,width)
    position = [0,0] #(y,x)
    randomField = ((0,0),(0,0))

    def __init__(self, field, safety, id ,fieldId):
        self.roomID = id
        self.fieldID = fieldId
        self.field = field
        self.roomID = id
        self.safety = safety
        self.initializing()

    def initializing(self):

        """
        :param field:       wird basis wie so definiert: ((y_min,x_min),(y_max,x_max)) also die diagonale Kante vom zufälligen Feld
        :param safety:      um den Fall zu vermeiden, dass 2 Räume nebeneinander erzeugt werden, dann wird der sichere Abstand  eingefügt
        :param color:       die Farbe von Raüme kontrollieren
        :return:
        """


        self.randomField = [(self.field[0][0] +  self.safety[0],self.field[0][1] +  self.safety[1]),(self.field[1][0] - (1 +  self.safety[0]),self.field[1][1] - (1 +  self.safety[1]))]
        self.position[0], self.position[1] = randint(self.randomField[0][0],self.randomField[1][0]) , randint(self.randomField[0][1],self.randomField[1][1])

        # Falls das zufällige Feld zu klein ist, passen sich die Breite und die Höhe von Räume an
        if ( self.safety[0] != 0 and  self.safety[1] != 0):
            if (self.field[1][0]%2 == 0):     self.shape[0] = randint( self.safety[0], self.safety[0]* 2)
            else:                             self.shape[0] = randint( self.safety[0],( self.safety[0]*2) - 1 )
            if (self.field[1][1]%2 == 0):     self.shape[1] = randint( self.safety[1], self.safety[1]* 2)
            else:                             self.shape[1] = randint( self.safety[1],( self.safety[1]*2) - 1 )
        else:
            self.shape[0] ,self.shape[1]  = randint(1,2), randint(1,2)

        # Falls 1 oder 2 Richtung von Räume neben der Grenze von der Karte
        if (self.position[0] -  int(self.shape[0]/2) <= self.field[0][0]):                      self.position[0] += 1
        if ((self.position[0] + (self.shape[0] - int(self.shape[0]/2))) >= self.field[1][0]):   self.position[0] -= 1
        if (self.position[1] - int(self.shape[1]/2) <= self.field[0][1]):                       self.position[1] += 1
        if ((self.position[1] + (self.shape[1] - int(self.shape[1]/2))) >= self.field[1][1]):   self.position[1] -= 1


        # Raum erstellen
        #self.dMap[y_pos - int(h/2):y_pos + (h - int(h/2)),x_pos - int(w/2):x_pos + (w - int(w/2))] = 7

    def mapImplement(self,map,value):

        #Map[y_pos - int(h/2):y_pos + (h - int(h/2)),x_pos - int(w/2):x_pos + (w - int(w/2))] = 7
        map[self.position[0] - int(self.shape[0]/2):self.position[0] + (self.shape[0] - int(self.shape[0]/2)),self.position[1] - int(self.shape[1]/2):self.position[1] + (self.shape[1] - int(self.shape[1]/2))] = value
        self.borderCalculating(map)



    def borderCalculating(self,map):


        top =       self.position[0] - int(self.shape[0]/2)
        bottom =    self.position[0] + (self.shape[0] - int(self.shape[0]/2))
        left =      self.position[1] - int(self.shape[1]/2)
        right =     self.position[1] + (self.shape[1] - int(self.shape[1]/2))


        for x_axis in range(left,right):

            if ((top - 1) >= 0 ):
                self.border.setdefault('top', []).append((top - 1, x_axis))

            if ((bottom + 1) <= np.shape(map)[0] ):
                 self.border.setdefault('bottom', []).append((bottom, x_axis))

        for y_axis in range(top,bottom):
            #print("x_axis = {} top = {} | bottom = {} ".format(y_axis,top,bottom))
            if ((left - 1) >= 0):
                self.border.setdefault('left', []).append((y_axis, left -1))
            if ((right + 1) <= np.shape(map)[1]):
                 self.border.setdefault('right', []).append((y_axis, right))

    def getID(self):
        temp = self.roomID
        return temp

    def getPosition(self):
        temp = self.position
        return temp

    def getShape(self):
        temp = self.shape
        return temp

    def getBorder(self,direction):
        if ((direction == 'top') or (direction == 'top') or (direction == 'top') or (direction == 'top')):
            temp = self.border.get(direction)
            return temp
        else:
            print ("Error!!!")
            return 0

class Dungeon:
    dMap =[]
    roomField =[]
    percentage = 50
    widthOfMap = 0
    heightOfMap = 0
    roads =[]
    borders = {}
    room = {}

    # Initialisierung vom Dungeon
    def __init__(self,width,height,percentage):

        self.percentage = int (percentage/10)
        self.widthOfMap = width
        self.heightOfMap = height
        temp = np.zeros((self.heightOfMap,self.widthOfMap), dtype=np.int)
        self.dMap = temp


    # mehrere Räume erstellen
    def multiRoom(self,interval,numberOfRoom):

        """
        :param interval         um die beste Weise von der Partition zu kontrollieren:
        :param numberOfRoom     die Anzahl von Räume:
        :return:
        """


        partition = self.roomPartition(self.factors(numberOfRoom),interval)
        count = numberOfRoom

        # die Faktoren werden von jeder Koordinate (x oder y) zufällig ausgewählt
        try:
            y_patition = choice(partition)
            partition.remove(y_patition)
            x_patition = choice(partition)
        except Exception as e:
            print("not acceptable!!!")
            return 0


        # die Karte wird kleiner geteilt
        y_axis = np.arange(0,self.heightOfMap + 1,int(self.heightOfMap / y_patition))
        x_axis = np.arange(0,self.widthOfMap + 1,int(self.widthOfMap / x_patition))

        # den Mangel ergänzen
        if (max(y_axis) != self.heightOfMap ):    y_axis[len(y_axis) -1 ] = self.heightOfMap
        if (max(x_axis) != self.widthOfMap ):    x_axis[len(x_axis) -1 ] = self.widthOfMap

        # die Liste von den zufälligen Feldern
        randomZone = []
        for r in range(1,len(y_axis)):
            for c in range(1,len(x_axis)):
                randomZone.append(((y_axis[r - 1] ,x_axis[c - 1]),((y_axis[r]  ,x_axis[c] ))))

        """
        + big, normal, small: die Größe von Räume kontrollieren
        - Normalerweise 30% von Räume sind größ, fast 50% sind durchschnittlich,  die übrigen sind Klein
        """

        big, normal, small = self.sizeControl(numberOfRoom)


        # Räume in den zufälligen Feldern erzeugt
        while (count !=  0):

            random = choice(randomZone)

            # größste Raum
            if (big != 0):

                b = Room(random,(floor((random[1][0] - random[0][0])/2 - 1),floor((random[1][1] - random[0][1])/2 - 1)),count,1)
                #print("field = {}, safe = {}, roomID = {}, fieldID = {}, shape = {}".format(b.field,b.safety,b.roomID,b.fieldID,b.shape))
                b.mapImplement(self.dMap,10)

                big -= 1

            # normale Raum
            elif(normal != 0):
                n = Room(random,(floor((random[1][0] - random[0][0])/2.5 - 1),floor((random[1][1] - random[0][1])/2.5 - 1)),count,1)
                #print("field = {}, safe = {}, roomID = {}, fieldID = {}, shape = {}".format(n.field,n.safety,n.roomID,n.fieldID,n.shape))
                n.mapImplement(self.dMap,5)
                normal -= 1

            # kleine Raum
            elif(small != 0):
                s = Room(random,(1,1),count,1)
                #print("field = {}, safe = {}, roomID = {}, fieldID = {}, shape = {}".format(s.field,s.safety,s.roomID,s.fieldID,s.shape))
                s.mapImplement(self.dMap,3)
                small -= 1

            randomZone.remove(random)
            count -= 1

        return self.dMap


    # 2 nächste Faktoren von der Anzahl des Raumes berechnen
    def factors(self, n):

        a = floor(sqrt(n))
        while(True):
            if ((n%a) == 0 ):
                b = int(n/a)
                return [a,b]
            else:
                a-=1

    # die Karte partitionieren
    def roomPartition(self, factor,interval):

        """
        :param factor:      nächste Faktoren von der Anzahl des Raumes
        :param interval:    größste Abstand von Partition suchen
        :return:

        """

        result = factor
        minimum = min(factor)
        candidate = (factor[0] * factor[1])

        for index in range(interval):
            candidate += 1

            if (min(self.factors(candidate)) > min(factor)):
                minimum = min(self.factors(candidate))
                result = self.factors(candidate)

        return result

    # Größe von Räume kontrollieren
    def sizeControl(self,numberOfRoom):
        if (numberOfRoom == 1): return [1,0,0]
        if (numberOfRoom == 2): return [1,1,0]
        if (numberOfRoom > 2):  return ceil((30 * numberOfRoom)/ 100), floor((50 * numberOfRoom)/ 100) ,abs(numberOfRoom - (ceil((30 * numberOfRoom)/ 100) + floor((50 * numberOfRoom)/ 100)))



    # Weg erstellen
    def roadCreating(self):

        r = Road(self.dMap)

        for key in self.borders.keys():
            if (key > min(self.borders.keys())):
                try:
                    #print(self.borders[key])
                    b = choice(self.borders[key])
                    c = choice(self.borders[key -1])
                    r.roadCreating(b,c,0,0)
                    r.fillRoad(b,c)
                    r.road =[]
                except RecursionError as re:
                    print('Sorry but this maze solver was not able to finish '
                     'analyzing the maze: {}'.format(re.args[0]))


    # Dungeon zurückgeben
    def returnArray(self):
        return self.dMap

    def fillBorder(self):
        for key in self.borders:
            for val in self.borders.get(key):

                self.dMap[val[0],val[1]] += 2

        return self.dMap

    def getBorder(self):
        return self.borders

if __name__ == '__main__':
    test = Dungeon(15,15,40)
    test.multiRoom(2,4)

    print(test.returnArray())
    print("\n")


    arr = test.returnArray()
    plt.imshow(arr, interpolation='nearest',cmap=plt.cm.gray)
    plt.show()

