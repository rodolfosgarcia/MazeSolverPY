import csv

class Rooms(object):
    def __init__(self, id, center, doors, link1, link2, link3, link4, link5, link6, parent=None):
        self.id = id.strip()
        self.center = center.strip()
        self.doors = []
        #self.doors = doors.split(',').strip()
        for door in doors.split(','):
            self.doors.append(door.strip())
        self.links = ['0', link1.strip(), link2.strip(), link3.strip(), link4.strip(), link5.strip(), link6.strip()]

        self.g = 0
        self.h = 0
        self.f = 0

        #store the Parent Room Object
        self.parent = parent







def AStar(maze, links, start, end):
    #maze is a dict of Rooms objects
    #start is the Room object
    #end is the Room object

    """Returns a list of Rooms IDs (str) as a path from the given start to the given end in the given maze"""

    start.g = 2000
    start.h = 2000
    start.f = start.g + start.h
    end.g = end.h = end.f = 0

    print(start.g)

    # Initialize both open and closed list
    openSet = []
    closedSet = []
    openSet.append(start)


    while len(openSet) > 0:
        # Get the current node
        currentRoom = openSet[0]
        currentIndex = 0
        print("********** " + currentRoom.center + " " + currentRoom.id + " **********")

        #update the curentRoom to the lowest f score
        for index, item in enumerate(openSet):
            #print("openSet " + item.center + "|f" + str(item.f))
            #print("Current " + currentRoom.center + "|f" + str(currentRoom.f))
            if item.f < currentRoom.f:
                currentRoom = item
                currentIndex = index


        if (currentRoom == end):
            #FINISHED! it found a path
            print ("FOUND IT")
            #checksum the parent links
            #for keyRoom in maze:
                #if maze[keyRoom].parent is not None:
                    #print ("center: " + maze[keyRoom].center + " | parent: " + maze[keyRoom].parent.center)
            CompleteReversePath = []
            blipsRoom = currentRoom
            print("currentRoom: " + blipsRoom.id)
            while blipsRoom is not None:
                if blipsRoom.center != 'Blank':
                    CompleteReversePath.append(blipsRoom.center)
                blipsRoom = blipsRoom.parent
                if blipsRoom is not None:
                    print("currentRoom: " + blipsRoom.id)
                else:
                    print("currentRoom: None")
            #CompleteReversePath.reverse()
            print ("Total Rooms passed:" + str(len(CompleteReversePath)))
            return CompleteReversePath


        # Pop current off open list, add to closed list
        openSet.pop(currentIndex)
        closedSet.append(currentRoom)




        #search for the link between current room and next room with open doors
        neighborsOfCurrent = []
        for door in currentRoom.doors:
            print(links[currentRoom.links[int(door)]])
            for NeighborId in links[currentRoom.links[int(door)]]:
                if currentRoom.id != NeighborId and links[currentRoom.links[int(door)]] != "UUUUUUU":
                    if maze[NeighborId] not in closedSet:
                        neighborsOfCurrent.append(maze[NeighborId])
                        maze[NeighborId].parent = currentRoom
                        print("neighbors " + maze[NeighborId].center + "|f" + str(maze[NeighborId].f) + "|pai " + str(maze[NeighborId].parent.center))






        for neighbor in neighborsOfCurrent:
            print(neighbor.center)
            #if Room already in closed set just ignore
            if neighbor in closedSet:
                #print("continue closedSet")
                continue

            #create f, g and h values
            temp_g = currentRoom.g + 1
            #print("temp_g: " + str(temp_g))
            #print("neighbor.g: " + str(neighbor.g))


            for openNeighbor in openSet:
                if neighbor == openNeighbor and neighbor.g > openNeighbor.g:
                    continue
            neighbor.g = temp_g
            neighbor.h = 25 - int(currentRoom.id[(len(currentRoom.id)-3)*-1:])
            print(str(currentRoom.id[(len(currentRoom.id)-3)*-1:]))
            neighbor.f = neighbor.g + neighbor.h
            print("adding to openSet")
            openSet.append(neighbor)




    #checksum the parent links
    #for keyRoom in maze:
        #if maze[keyRoom].parent is not None:
            #print ("center: " + maze[keyRoom].center + " | parent: " + maze[keyRoom].parent.center)




    return ("path not found")




def populateMazeLinks(dict, link, id):
    if link != "BBBBBBB":
        if link in dict:
            dict[link].append(id)
        else:
            dict[link] = [id]



def main():

    mazeMap = {}
    mazeLinks = {}

    with open('MazeInput.csv', mode='r', newline='') as infile:
        csv_reader = csv.DictReader(infile)
        for row in csv_reader:
            room = Rooms(row['ID'], row['CENTER'], row['DOORS'], row['LINK1'], row['LINK2'], row['LINK3'], row['LINK4'], row['LINK5'], row['LINK6'])
            mazeMap[row['ID']] = room
            populateMazeLinks(mazeLinks, row['LINK1'], row['ID'])
            populateMazeLinks(mazeLinks, row['LINK2'], row['ID'])
            populateMazeLinks(mazeLinks, row['LINK3'], row['ID'])
            populateMazeLinks(mazeLinks, row['LINK4'], row['ID'])
            populateMazeLinks(mazeLinks, row['LINK5'], row['ID'])
            populateMazeLinks(mazeLinks, row['LINK6'], row['ID'])
        startRoom = mazeMap['ROW23']
        endRoom = mazeMap['ROW907']

    path = AStar(mazeMap, mazeLinks, startRoom, endRoom)
    print(path)


if __name__ == '__main__':
    main()
