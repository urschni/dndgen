__author__ = 'tunghoang'
from random import randint, choice
from math import *
import numpy as np
import matplotlib.pyplot as plt
#from Road import Road
"""
Dnd Generator version 0.054
"""

class Dungeon:
    dMap =[]
    roomField =[]
    percentage = 50
    widthOfMap = 0
    heightOfMap = 0
    roads =[]
    borders = {}

    # Initialisierung vom Dungeon
    def __init__(self,width,height,percentage):

        self.percentage = int (percentage/10)
        self.widthOfMap = width
        self.heightOfMap = height
        temp = np.zeros((self.heightOfMap,self.widthOfMap), dtype=np.int)
        self.dMap = temp




    # Initialisierung vom Raum
    def roomInitializing(self,field, safety,color):

        """
        :param field:       wird basis wie so definiert: ((y_min,x_min),(y_max,x_max)) also die diagonale Kante vom zufälligen Feld
        :param safety:      um den Fall zu vermeiden, dass 2 Räume nebeneinander erzeugt werden, dann wird der sichere Abstand  eingefügt
        :param color:       die Farbe von Raüme kontrollieren
        :return:
        """


        randomfield = [(field[0][0] +  safety[0],field[0][1] +  safety[1]),(field[1][0] - (1 +  safety[0]),field[1][1] - (1 +  safety[1]))]
        y_pos, x_pos = randint(randomfield[0][0],randomfield[1][0]) , randint(randomfield[0][1],randomfield[1][1])

        # Falls das zufällige Feld zu klein ist, passen sich die Breite und die Höhe von Räume an
        if ( safety[0] != 0 and  safety[1] != 0):
            if (field[1][0]%2 == 0):     h = randint( safety[0], safety[0]* 2)
            else:                        h = randint( safety[0],( safety[0]*2) - 1 )
            if (field[1][1]%2 == 0):     w = randint( safety[1], safety[1]* 2)
            else:                        w = randint( safety[1],( safety[1]*2) - 1 )
        else:
            h,w = randint(1,2), randint(1,2)

        # Falls 1 oder 2 Richtung von Räume neben der Grenze von der Karte
        if (y_pos - int(h/2) <= field[0][0]):           y_pos += 1
        if ((y_pos + (h - int(h/2))) >= field[1][0]):   y_pos -= 1
        if (x_pos - int(w/2) <= field[0][1]):           x_pos += 1
        if ((x_pos + (w - int(w/2))) >= field[1][1]):   x_pos -= 1


        # Grenze wird erzeugt, dann kann ein zufällige Knoten davon ausgewählt werden, um start- oder ende- Knoten zu werden
        self.borderCalculating(x_pos, y_pos, w, h, color)

        # Raum erstellen
        self.dMap[y_pos - int(h/2):y_pos + (h - int(h/2)),x_pos - int(w/2):x_pos + (w - int(w/2))] = 10




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
                self.roomInitializing(random,(floor((random[1][0] - random[0][0])/2 - 1),floor((random[1][1] - random[0][1])/2 - 1)),5)
                big -= 1

            # normale Raum
            elif(normal != 0):
                self.roomInitializing(random,(floor((random[1][0] - random[0][0])/3 - 1),floor((random[1][1] - random[0][1])/3 - 1)),5)
                normal -= 1

            # kleine Raum
            elif(small != 0):
                self.roomInitializing(random,(1,1),count)
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


    # die Grenze berechen
    def borderCalculating(self, x_pos, y_pos, width, height, index ):


        top = y_pos - int(height/2)
        bottom = y_pos + (height - int(height/2))
        left = x_pos - int(width/2)
        right = x_pos + (width - int(width/2))


        for x_axis in range(left,right):

            if ((top - 1) >= 0 ):
                self.borders.setdefault(index, []).append((top - 1, x_axis))

            if ((bottom + 1) <= self.widthOfMap ):
                self.borders.setdefault(index, []).append((bottom, x_axis))

        for y_axis in range(top,bottom):
            #print("x_axis = {} top = {} | bottom = {} ".format(y_axis,top,bottom))
            if ((left - 1) >= 0):
                self.borders.setdefault(index, []).append((y_axis, left -1))
            if ((right + 1) <= self.heightOfMap):
                self.borders.setdefault(index, []).append((y_axis, right))


    # Weg erstellen
    def roadCreating(self):
        print(self.borders)
        for key in range(1,len(self.borders)):
            start = self.borders.get(key)[0]
            end = self.borders.get(key+1)[1]#randint(0,len(self.borders.get(key+1)))
            print(start)
            print(end)

            #road = Road(self.dMap,start,end)
            #road.fillRoad(self.dMap)
            #self.roads.append(road)


    # Dungeon zurückgeben
    def returnArray(self):
        return self.dMap

    def fillBorder(self):
        for key in self.borders:
            for val in self.borders.get(key):

                self.dMap[val[0],val[1]] += 2.5

        return self.dMap

    def getBorder(self):
        return self.borders

if __name__ == '__main__':
    test = Dungeon(10,10,40)
    test.multiRoom(2,5)
    #y,x,h,w = test.roomInitializing(((0,0),(10,10)),(3,3),1)
    #print( y,x,h,w)

    print("\n")

    b = test.returnArray()

    test.fillBorder()



    arr = test.returnArray()
    plt.imshow(arr, interpolation='nearest',cmap=plt.cm.gray)
    plt.show()

