__author__ = 'tunghoang'
from random import randint, choice
from Road import *
from math import *
import numpy as np
import matplotlib.pyplot as plt

"""
Dnd Generator version 0.060
"""
class Room(object):
    roomID = 0
    fieldID = 0
    field = ((0,0),(0,0))
    randomField = ((0,0),(0,0))

    def __init__(self, field, safety, id ,fieldId,neighbor):
        self.roomID = id
        self.fieldID = fieldId
        self.field = field
        self.roomID = id
        self.safety = safety
        self.neighbor = neighbor
        self.shape = [0,0]    #(height,width)
        self.position = [0,0] #(y,x)
        self.border ={}
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

    def __repr__(self):
        return ('id: {}, position: {}, shape: {}, fieldID: {}, nearby: {} '.format(self.roomID,self.position,self.shape,self.fieldID,self.neighbor))

    def getID(self):
        temp = self.roomID
        return temp

    def getPosition(self):
        temp = self.position
        return temp

    def getShape(self):

        temp = self.shape
        print(temp)
        return test

    def getNeighbor(self):
        temp = self.neighbor
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
    compare = []
    percentage = 50
    widthOfMap = 0
    heightOfMap = 0
    roads =[]
    rooms = []
    max = 0

    # Initialisierung vom Dungeon
    def __init__(self,width,height,percentage):

        self.compare = [width,height]
        if (min(self.compare) >= floor(max(self.compare)/3)):
            self.widthOfMap = width
            self.heightOfMap = height
            self.max = floor((width/3) *(height/3))
        else:
            print("Error!!!")
            return

        self.percentage = int (percentage/10)
        temp = np.zeros((self.heightOfMap,self.widthOfMap), dtype=np.int)
        self.dMap = temp


    # mehrere Räume erstellen
    def multiRoom(self,interval,numberOfRoom):

        """
        :param interval         um die beste Weise von der Partition zu kontrollieren:
        :param numberOfRoom     die Anzahl von Räume:
        :return:
        """
        if (numberOfRoom > self.max):
            numberOfRoom = self.roomDescrement(numberOfRoom)

        partition = self.roomPartition(self.factors(numberOfRoom),interval)
        print(partition)
        count = numberOfRoom

        # die Faktoren werden von jeder Koordinate (x oder y) zufällig ausgewählt
        try:
            if (min(self.compare) == max(self.compare)):
                y_patition = choice(partition)
                partition.remove(y_patition)
                x_patition = choice(partition)
            else:
                if (max(self.compare) == self.heightOfMap):
                    y_patition, x_patition = max(partition), min(partition)
                else:
                    y_patition, x_patition = min(partition), max(partition)

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
        randomZone = {}
        neighbor  = {}
        i = 0
        mapping = np.zeros((len(y_axis)-1,len(x_axis) - 1), dtype = np.int)

        for row in range(1,len(y_axis)):
            for column in range(1,len(x_axis)):

                i += 1
                mapping[row-1][column-1] = i
                randomZone.setdefault(i ,((y_axis[row - 1] ,x_axis[column - 1]),((y_axis[row]  ,x_axis[column] ))))


        for r in range(len(y_axis)-1):
            for c in range(len(x_axis)-1):
                try:
                    if (r - 1  >= 0):   neighbor.setdefault(mapping[r][c],[]).append(mapping[r -1][c])          #top
                    if (c - 1 >= 0):    neighbor.setdefault(mapping[r][c],[]).append(mapping[r    ][c - 1])     #left
                    if (c-1 >= 0) : neighbor.setdefault(mapping[r][c],[]).append(mapping[r + 1][c])             #bottom
                    neighbor.setdefault(mapping[r][c],[]).append(mapping[r    ][c + 1])                         #right

                except IndexError:
                    pass


        """
        + big, normal, small: die Größe von Räume kontrollieren
        - Normalerweise 30% von Räume sind größ, fast 50% sind durchschnittlich,  die übrigen sind Klein
        """

        big, normal, small = self.sizeControl(numberOfRoom)


        # Räume in den zufälligen Feldern erzeugt
        while (count !=  0):
            key =   choice(list(randomZone))
            random = randomZone.get(key)

            # größste Raum
            if (big != 0):

                b = Room(random,(floor((random[1][0] - random[0][0])/2 - 1),floor((random[1][1] - random[0][1])/2 - 1)),count, key, neighbor.get(key))
                self.rooms.append(b)
                b.mapImplement(self.dMap,10)
                big -= 1

            # normale Raum
            elif(normal != 0):
                n = Room(random,(floor((random[1][0] - random[0][0])/2.5 - 1),floor((random[1][1] - random[0][1])/2.5 - 1)),count,key,neighbor.get(key))
                self.rooms.append(n)
                n.mapImplement(self.dMap,10)
                normal -= 1

            # kleine Raum
            elif(small != 0):
                s = Room(random,(1,1),count,key,neighbor.get(key))
                self.rooms.append(s)
                s.mapImplement(self.dMap,10)
                small -= 1

            try:
                del randomZone[key]
            except KeyError:
                pass
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

        result = factor
        minimum = min(factor)
        candidate = (factor[0] * factor[1])

        if (min(self.compare) <= floor(max(self.compare)/3 * 2)):

            if (candidate < 4 ):    return factor
            elif (candidate >= 4 and candidate < 15):
                if (candidate%2) == 0:
                    return factor
                else:
                    temp = self.ratioControl(self.factors(candidate+1))
                    if (min(temp) >= 3):
                        return self.factors(candidate+1)
                    else:
                        return self.roomDescrement(candidate)

        for index in range(interval):
            candidate += 1
            temp = self.ratioControl(self.factors(candidate))

            if (min(self.factors(candidate)) > min(factor)):
                if (min(temp) >= 3):
                    if (max(self.factors(candidate)) < max(result)):
                        minimum = min(self.factors(candidate))
                        result = self.factors(candidate)
                    else:
                        return result
                else:
                    return self.roomDescrement(candidate)
        return result


    # Größe von Räume kontrollieren
    def ratioControl(self,factor):
        return [floor(max(self.compare)/max(factor)),floor(min(self.compare)/min(factor))]

    def roomDescrement(self,candidate):

        while (min(self.ratioControl(self.factors(candidate))) < 3):
            candidate -= 1

        return self.factors(candidate)

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


if __name__ == '__main__':
    test = Dungeon(30,18,40)
    test.multiRoom(5,6)
    for r in test.rooms:
        print(r)

    arr = test.returnArray()
    plt.imshow(arr, interpolation='nearest',cmap=plt.cm.gray)
    plt.show()

