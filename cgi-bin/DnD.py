
__author__ = 'tunghoang'
from random import randint, choice
from Road import *
from math import *
import numpy as np
import matplotlib.pyplot as plt

"""
Dnd Generator version 0.80
"""
class Room(object):

    def __init__(self, field, safety, id ,fieldId, neighbor, nDirection):
        self.roads = []
        self.nDirection = nDirection
        self.roomID = id
        self.fieldID = fieldId
        self.field = field
        self.roomID = id
        self.safety = safety
        self.neighbor = neighbor
        self.shape = [0,0]    #(height,width)
        self.position = [0,0] #(y,x)
        self.border ={}
        self.coordinates = []
        self.doors = {}
        self.initializing()


    def cornerSetup(self):
        self.top =      self.position[0] - int(self.shape[0]/2)
        self.bottom =    self.position[0] + (self.shape[0] - int(self.shape[0]/2))
        self.left =      self.position[1] - int(self.shape[1]/2)
        self.right =     self.position[1] + (self.shape[1] - int(self.shape[1]/2))



    def shapeSetup(self):
        # Falls das zufällige Feld zu klein ist, passen sich die Breite und die Höhe von Räume an
        if ( self.safety[0] != 0 and  self.safety[1] != 0):
            if (self.field[1][0]%2 == 0):     self.shape[0] = randint( self.safety[0], self.safety[0]* 2)
            else:                             self.shape[0] = randint( self.safety[0],( self.safety[0]*2) - 1 )
            if (self.field[1][1]%2 == 0):     self.shape[1] = randint( self.safety[1], self.safety[1]* 2)
            else:                             self.shape[1] = randint( self.safety[1],( self.safety[1]*2) - 1 )
        else:
            self.shape[0] ,self.shape[1]  = randint(1,2), randint(1,2)



    def positionAdjustment(self):
        # Falls 1 oder 2 Richtung von Räume neben der Grenze von der Karte
        if (self.position[0] -  int(self.shape[0]/2) <= self.field[0][0]):                      self.position[0] += 1
        if ((self.position[0] + (self.shape[0] - int(self.shape[0]/2))) >= self.field[1][0]):   self.position[0] -= 1
        if (self.position[1] - int(self.shape[1]/2) <= self.field[0][1]):                       self.position[1] += 1
        if ((self.position[1] + (self.shape[1] - int(self.shape[1]/2))) >= self.field[1][1]):   self.position[1] -= 1



    def initializing(self):
        """
        :param field:       wird basis wie so definiert: ((y_min,x_min),(y_max,x_max)) also die diagonale Kante vom zufälligen Feld
        :param safety:      um den Fall zu vermeiden, dass 2 Räume nebeneinander erzeugt werden, dann wird der sichere Abstand  eingefügt
        :param color:       die Farbe von Raüme kontrollieren
        :return:
        """
        self.randomField = [(self.field[0][0] +  self.safety[0],self.field[0][1] +  self.safety[1]),(self.field[1][0] - (1 +  self.safety[0]),self.field[1][1] - (1 +  self.safety[1]))]
        self.position[0], self.position[1] = randint(self.randomField[0][0],self.randomField[1][0]) , randint(self.randomField[0][1],self.randomField[1][1])

        self.shapeSetup()
        self.positionAdjustment()
        self.cornerSetup()

        for y_axis in range(self.top,self.bottom):
            for x_axis in range(self.left,self.right):
                self.coordinates.append((y_axis,x_axis))

        # Raum erstellen
        #self.dMap[y_pos - int(h/2):y_pos + (h - int(h/2)),x_pos - int(w/2):x_pos + (w - int(w/2))] = 7



    def mapImplement(self,map,value):

        #Map[y_pos - int(h/2):y_pos + (h - int(h/2)),x_pos - int(w/2):x_pos + (w - int(w/2))] = 7
        map[self.position[0] - int(self.shape[0]/2):self.position[0] + (self.shape[0] - int(self.shape[0]/2)),self.position[1] - int(self.shape[1]/2):self.position[1] + (self.shape[1] - int(self.shape[1]/2))] = value
        self.borderCalculating(map)



    def borderCalculating(self,map):

        for x_axis in range(self.left, self.right):
            if ((self.top - 1) >= 0 ):
                self.border.setdefault( (0,-1), []).append((self.top - 1, x_axis))   #top

            if ((self.bottom + 1) <= np.shape(map)[0] ):
                self.border.setdefault((0,1), []).append((self.bottom, x_axis))      #bottom

        for y_axis in range(self.top,self.bottom):
            if ((self.left - 1) >= 0):
                self.border.setdefault( (1,-1), []).append((y_axis, self.left -1))   #left
            if ((self.right + 1) <= np.shape(map)[1]):
                self.border.setdefault((1,1), []).append((y_axis, self.right))       #right

        for i in self.border.keys():
            self.doors.setdefault(i,[]).append(choice(self.border.get(i)))


    def fillBorder(self,map):
        for i in self.border.keys():
            for coordinate in self.border.get(i):
                map[coordinate[0]][coordinate[1]] += 3


    def __repr__(self):
        return ('id: {}, position: {}, shape: {}, fieldID: {}, nearby: {} '.format(self.roomID,self.position,self.shape,self.fieldID,self.neighbor))

    def getDoors(self):
        return self.doors

    def getID(self):
        return self.roomID

    def getNeightbor(self):
        return self.neighbor

    def getBorder(self,direction):
        if (direction == True): return self.border
        if ((direction == 2) or (direction == -2) or (direction == 1) or (direction == -1)):
            temp = self.border.get(direction)
            return temp
        else:
            print ("Error!!!")
            return 0

    def getCorner(self):
        return [(self.top,self.left),(self.bottom, self.right)]

    def addRoad(self, road):
        if len(self.roads) <= len(self.neighbor):
            self.roads.append(road)
        return 0




class Dungeon(object):


    # Initialisierung vom Dungeon
    def __init__(self,width,height,*dePercent):
        self.dMap =[]
        self.roads =[]
        self.rooms = []
        self.shape = [height,width]
        if (min(self.shape) >= floor(max(self.shape)/3)):
            self.shape[0] = height
            self.shape[1] = width
            self.max = floor((width/3) *(height/3))
        else:
            print("Error!!!")
            return

        if dePercent:
            if dePercent[0] >= 0 or dePercent[0] <= 100:
                self.deFrequency = dePercent[0]
        else:
            self.deFrequency = 50
        self.deadends = []
        self.dMap = np.zeros((self.shape[0],self.shape[1]), dtype=np.int)
        self.id = []



    # mehrere Räume erstellen
    def multiRoom(self,interval,numberOfRoom):

        if (numberOfRoom > self.max):
            numberOfRoom = self.max

        self.partition = self.roomPartition(self.factors(numberOfRoom),interval)
        count = numberOfRoom

        # die Faktoren werden von jeder Koordinate (x oder y) zufällig ausgewählt
        try:
            if (self.shape[0] == self.shape[1]):
                y_patition = choice(self.partition)
                self.partition.remove(y_patition)
                x_patition = self.partition[0]

            elif (self.shape.index(max(self.shape)) == 0):
                y_patition, x_patition = max(self.partition), min(self.partition)

            else:
                y_patition, x_patition = min(self.partition), max(self.partition)

        except Exception as e:
            print("not acceptable!!!")
            return 0


        self.mapping((y_patition,x_patition))
        """
        + big, normal, small: die Größe von Räume kontrollieren
        - Normalerweise 30% von Räume sind größ, fast 50% sind durchschnittlich,  die übrigen sind Klein
        """

        big, normal, small = self.sizeControl(numberOfRoom)
        id = [elementID for elementID in self.id]
        if count > len(id):
            count = len(id)
        safetyFactor = [2,2.5]

        safetyFactor = [2,2.5]
        # Räume in den zufälligen Feldern erzeugt

        while (count !=  0):
            key = choice(id)

            keyCo = self.mappingCo.get(key) #key Coordinates
            id.remove(key)                  # remove id

            start = self.mapping[keyCo[0]][keyCo[1]]['randomZone'][0]
            end = self.mapping[keyCo[0]][keyCo[1]]['randomZone'][1]
            nearbyField = self.mapping[keyCo[0]][keyCo[1]]['neightbor']
            nearbyDirection = self.mapping[keyCo[0]][keyCo[1]]['neightbor']


            # größste Raum
            if (big != 0):

                b = Room((start,end),(floor(abs(start[0] - end[0])/safetyFactor[0] - 1),floor(abs(start[1] - end[1])/safetyFactor[0] - 1)),count, key, nearbyField ,nearbyDirection)
                self.mapping[keyCo[0]][keyCo[1]]['room'] = count
                b.mapImplement(self.dMap,10)
                self.rooms.append(b)

                big -= 1

            # normale Raum
            elif(normal != 0):

                n = Room((start,end),(floor(abs(start[0] - end[0])/safetyFactor[1] - 1),floor(abs(start[1] - end[1])/safetyFactor[1] - 1)),count, key, nearbyField ,nearbyDirection)
                self.mapping[keyCo[0]][keyCo[1]]['room'] = count
                n.mapImplement(self.dMap,10)
                self.rooms.append(n)

                normal -= 1

            # kleine Raum
            elif(small != 0):
                s = Room((start,end),(1,1),count,key,nearbyField ,nearbyDirection)
                self.mapping[keyCo[0]][keyCo[1]]['room'] = count
                s.mapImplement(self.dMap,10)
                self.rooms.append(s)

                small -= 1

            count -= 1

            self.rooms = sorted(self.rooms,key = lambda x: x.getID())

        self.dataConverting()

        return self.dMap


    def mapping(self,partition):

        # die Karte wird kleiner geteilt
        y_axis = np.arange(0,self.shape[0] + 1,int(self.shape[0] / partition[0]))
        x_axis = np.arange(0,self.shape[1] + 1,int(self.shape[1] / partition[1]))

        # den Mangel ergänzen
        if (max(y_axis) != self.shape[0] ):    y_axis[len(y_axis) -1 ] = self.shape[0]
        if (max(x_axis) != self.shape[1] ):    x_axis[len(x_axis) -1 ] = self.shape[1]


        # die Liste von den zufälligen Feldern
        self.mappingCo = {}  # mappingCOordinates
        fieldID = 0

        # map
        self.mapping = np.zeros((len(y_axis)-1,len(x_axis) - 1), dtype = object)

        mappingShape = np.shape(self.mapping)

        for row in range(0, mappingShape[0]):
            for column in range(0,mappingShape[1]):

                limit = [   ( y_axis[row],      x_axis[column]),            #root
                            ( y_axis[row + 1] , x_axis[column + 1] )    ]   #limit

                self.mapping[row][column] = {'fieldID': fieldID, 'randomZone': [], 'neightbor': [], 'neightborDirection' : [], 'room': 0}
                self.mapping[row][column]['randomZone'].extend(limit)
                self.mappingCo.setdefault(fieldID, []).extend([row,column])
                
                self.id.append(fieldID)
                fieldID += 1



        for row in range(0, mappingShape[0]):
            for column in range(0,mappingShape[1]):

                neighbor  = [(row + 1 , column,     mappingShape[0],    0),       #bottom
                             (row - 1 , column,     mappingShape[0],    0),       #top
                             (row ,     column + 1, mappingShape[1],    1),       #right
                             (row ,     column - 1, mappingShape[1],    1)  ]     #left

                nd = [(0,1),(0,-1),(1,1),(1,-1),]

                #neightborDirection
                for c in range(len(neighbor)):
                    axis = neighbor[c][3]
                    if (neighbor[c][axis] > -1 and (neighbor[c][axis] < neighbor[c][2])):
                        self.mapping[row][column]['neightbor'].append(self.mapping[neighbor[c][0]][neighbor[c][1]]['fieldID'])
                        self.mapping[row][column]['neightborDirection'].append(nd[c])


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

        if (min(self.shape) <= floor(max(self.shape)/3 * 2)):

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
        return [floor(max(self.shape)/max(factor)),floor(min(self.shape)/min(factor))]

    def roomDescrement(self,candidate):

        while (min(self.ratioControl(self.factors(candidate))) < 3):
            candidate -= 1

        return self.factors(candidate)

    def sizeControl(self,numberOfRoom):
        if (numberOfRoom == 1): return [1,0,0]
        if (numberOfRoom == 2): return [1,1,0]
        if (numberOfRoom > 2):  return ceil((30 * numberOfRoom)/ 100), floor((50 * numberOfRoom)/ 100) ,abs(numberOfRoom - (ceil((30 * numberOfRoom)/ 100) + floor((50 * numberOfRoom)/ 100)))

    def dataConverting(self):

        shape =     np.shape(self.mapping)
        temp =      np.reshape(self.mapping,(1,shape[0] * shape[1]))

        for i in temp[0]:

            roomID = i.get('room') - 1
            i.setdefault('doors')
            i['doors'] = self.rooms[roomID].getDoors()

        self.mapping = temp



    def roadCreating(self):


        for field in self.mapping[0]:

            startCandidates = field.get('neightborDirection')
            startNeightbor = field.get('neightbor')

            if field.get('room') != 0:

                while len(startNeightbor) != 0:

                    startFieldID = field.get('fieldID')
                    endFieldID = field.get('neightbor')[0]

                    startDirection = startCandidates[0]
                    start = field.get('doors').get(startDirection)[0]



                    endFieldSelected = self.mapping[0][endFieldID]
                    endDirection = (startCandidates[0][0],startCandidates[0][1] * -1)
                    endRoom = endFieldSelected.get('room')

                    if endRoom == 0:
                      
                        startNeightbor.remove(endFieldID)   
                        startCandidates.remove(startDirection)
                        endFieldSelected.get('neightbor').remove(startFieldID)
                        endFieldSelected.get('neightborDirection').remove(endDirection)

                    else:
                        
                        end  = endFieldSelected.get('doors').get(endDirection)[0]
                        startNeightbor.remove(endFieldID)
                        startCandidates.remove(startDirection)

                        endFieldSelected.get('neightbor').remove(startFieldID)
                        endFieldSelected.get('neightborDirection').remove(endDirection)
                        #def __init__(self, map, start, end, roadID,startingRoomID,destinationID):
                        tempRoad = Road(self.dMap,start,end,1,startFieldID,endFieldID)
                        self.roads.append(tempRoad)


        self.roads.append(self.entranceCreating())
        self.roads.append(self.exitCreating())
        self.deadends.extend(self.deadendSetup())


        self.printRoad()

    # Dungeon zurückgeben
    def returnArray(self):
        return self.dMap

    def printRoad(self):

        for road in self.roads:

            listNode = road.getRoad()
            max = len(listNode)

            for n in range(max):
                if ((n > 0) and (n < max - 1)):
                    self.dMap[listNode[n][0]][listNode[n][1]] = 3
                else:
                    self.dMap[listNode[n][0]][listNode[n][1]] = 6

        for de in self.deadends:

            listNode = de.getRoad()
            max = len(listNode)

            for n in range(max):

                self.dMap[listNode[n][0]][listNode[n][1]] = 3


        return self.dMap

    def getCorner(self):

        self.corner = {}
        for room in self.rooms:

            id = room.getID()
            corner = room.getCorner()
            self.corner.setdefault(id,[]).extend(corner)

        return self.corner


    def exitCreating(self):


        directionList = [(1,1),(0,1)]
        direction = choice(directionList)
        print(direction)

        for f in range(len(self.mapping[0])-1,-1,-1):
            room = self.mapping[0][f].get('room')
            if room != 0:
                startNode = self.mapping[0][f].get('doors').get(direction)[0]
                roomID = self.mapping[0][f].get('room')

                endNode = [self.shape[0] -1,self.shape[1] -1]

                #def __init__(self, map, start, end, roadID,startingRoomID,destinationID):
                exit = Road(self.dMap,startNode,endNode,-1,-1,roomID)

                break

        return exit

    def entranceCreating(self):

        directionList = [(1,1),(0,1)]
        direction = choice(directionList)
        reversedDirection = (direction[0],direction[1] * -1)

        endNode = self.mapping[0][0].get('doors').get(reversedDirection)[0]
        roomID = self.mapping[0][0].get('room')

        ##def __init__(self, map, start, end, roadID,startingRoomID,destinationID):
        entrance = Road(self.dMap,(0,0),endNode,-1,-1,roomID)


        return entrance

    def deadendSetup(self):

        count = 0
        print(len(self.roads))
        self.deadendsMax = floor(len(self.roads)/100 * self.deFrequency)

        print(self.deadendsMax)

        selectedList = []

        for roadIdx in range(0,len(self.roads)-2):
            selectedList.append(self.roads[roadIdx])


        while(count < self.deadendsMax):

            target = choice(selectedList)
            targetID = target.getRoadID()

            startID = target.getFromID()
            endID = target.getToID()
            keysList = target.getMid()
            limit = target.getLimit()
            #def __init__(self, map, start, end, roadID,startingRoomID,destinationID,*randomRoad):
            deadend = Road(self.dMap,keysList[0],keysList[1],(targetID + len(self.roads) * 2),startID,endID,limit)

            self.deadends.append(deadend)
            selectedList.remove(target)
            count += 1



        return self.deadends



if __name__ == '__main__':

    test = Dungeon(50,50)
    test.multiRoom(5,12)

    test.roadCreating()




    arr = test.returnArray()
    plt.imshow(arr, interpolation='nearest',cmap=plt.cm.gray)
    plt.show()

