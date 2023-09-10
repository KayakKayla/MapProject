from PIL import Image, ImageDraw
import re
class Graph:
    def __init__(self):  # add a dictionary with all the nodes
        # has name and location of node
        self.nodes = {}
        self.locations = {}
        self.types = {"Classroom": [],
                      "Hallway": [],
                      "Stairs": [],
                      "Special": [],
                      "Elevator": []}
        
    def importNodes(self, csvFile):
        f = open(csvFile, "r")
        keys = {}
        list = []
        for line in f:
            information = line.split(",")
            name = information[0]
            nodeType = information[1]
            if nodeType == "Classroom":
                alternativeName = re.sub(r"[\n\t\s]*", "", information[5])
                if alternativeName != "":
                    keys[alternativeName] = name
                    list.append(alternativeName)
                else:
                    keys[name] = name
                    list.append(name)
            CoOrdinates = [int(x) for x in information[2].split()]
            self.locations[name] = CoOrdinates
            connectionNames = information[3].split()
            connectionDistances = [int(x) for x in information[4].split()]
            self.addNode(name, nodeType, connectionNames, connectionDistances)
        return list, keys

    def addNode(self, name, type="Classroom", connections=["Z"], distances=[0]):
        self.nodes[name] = Node(name, type)
        self.types[type].append(name)

        # self.types[type].append(name)  # figure out if you should use name or actual node
        for i in range(len(connections)):
            self.nodes[name].addConnection(connections[i], distances[i])

    def display(self):
        for key in self.nodes:
            print(f"{self.nodes[key].data()}")

    def classExists(self, classroom):
        if classroom in self.nodes:
            return True
        return False

    def displayPath(self, startPoint, endPoint):
        result = self.findPath(startPoint, endPoint)
        image = Image.open('FullFloor.png')
        draw = ImageDraw.Draw(image)
        for i in range(len(result) - 1):
            if result[i] != "B1Aud" and result[i+1] != "B1Aud":
                if self.nodes[result[i]].type == "Stairs" and self.nodes[result[i+1]].type == "Stairs":
                    pass
                else:
                    draw.line(self.locations[result[i]] + self.locations[result[i + 1]], fill=100, width=2)
        image.save(f"images/{startPoint}_{endPoint}.png")

    def findPath(self, startPoint, endPoint):
        # while end not found?
        # Turn off all classroom nodes that aren't the one
        beginning = self.nodes[startPoint].name
        start = self.nodes[startPoint]
        end = self.nodes[endPoint]
        extra = []
        if "Aud" in startPoint or "Aud" in endPoint:
            extra += ["hB19", "hB16", "B2Aud", "B2Aud1", "B1Aud"]
        if startPoint == "C1Caf" or endPoint == "C1Caf":
            extra += ["hC2","hC3"]
        distance = dict.fromkeys(self.types["Hallway"] + self.types["Stairs"] + [startPoint, endPoint, "A1Lib"]+extra,
                                 [9999999999, "none"])  # set all distances to infinity, also optimized to not include other classrooms
        unexplored = dict.fromkeys(distance, 9999999999)  # there has to be a better w ay
        distance[start.name] = [0, start.name]
        # unexplored.pop(start.name)
        # minUnexplored = min(unexplored, key=unexplored.get)
        # start = self.nodes[minUnexplored]  # then repeat
        # print(start.name)
        while start.name != end.name:
            # print(start.name)
            for room in start.connections:
                # start.connections[room]+distance[start.name][0] adds distance from previous point to current point
                # improve it later so that it has no stuff
                if room in unexplored:
                    # print(room)
                    if start.connections[room] + distance[start.name][0] < distance[room][0]:
                        distance[room] = [start.connections[room] + distance[start.name][0], start.name]
                        unexplored[room] = start.connections[room] + distance[start.name][0]
            unexplored.pop(start.name)  # removes the point that has already been explored
            minUnexplored = min(unexplored, key=unexplored.get)  # finds the minimum pont that hasn't been explored yet
            start = self.nodes[minUnexplored]  # finds the new starting point
        # print("------------------")
        # print(distance)
        point = end.name
        path = []
        while point != beginning:
            path.insert(0, point)
            # print(point, distance[point])
            point = distance[point][1]
        path.insert(0, beginning)
        return path


class Node:
    def __init__(self, name, type="classroom"):
        self.name = name
        self.type = type  # classroom, hallway, stairs, elevator
        self.connections = {}

    def addConnection(self, nodeName, distance):
        self.connections[nodeName] = distance

    def data(self):
        return f"{self.name}: {self.type}, {self.connections}"