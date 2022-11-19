import json
import math

class Track:

    track = 0
    curr = "S0"
    name = {}
    pit = "nopit";  #nopit, pit
    fork1 = "left"; #left, middle, right
    fork2 = "left"; #left, right
    fork3 = "left"; #left, right

    # 
    def __init__(self, trackName):
        with open("app/track/" + trackName + ".geojson", "r") as f:
            self.track = json.load(f)
        for i in range(len(self.track["features"])):
            self.name.update({self.track["features"][i]["properties"]["name"]: i})
    
    # example call setFork("right", "right", "right") takes the longest route
    def setForks(self, f1, f2, f3):
        self.fork1 = f1
        self.fork2 = f2
        self.fork3 = f3

    # example call pitNext() forces car to take the ONLY the next pit
    def pitNext(self):
        self.pit = "pit"

    # returns current name like "S0"
    def getCurr(self):
        return self.curr

    # returns next name like "S1"
    def getNext(self, p1=None):
        if(p1 == None):
            p1 = self.curr
        match = lambda s: self._getPoint(p1)["properties"]["name"] == s
        if(match("S5")):
            return self._getPoint(p1)["properties"][self.fork1]
        if(match("S8")):
            return self._getPoint(p1)["properties"][self.fork2]
        if(match("S10")):
            return self._getPoint(p1)["properties"][self.fork3]
        if(match("S21")):
            if(self.pit == "pit"):
                self.pit = "nopit"
                return self._getPoint(p1)["properties"]["pit"]
            return self._getPoint(p1)["properties"]["nopit"]
        return self._getPoint(p1)["properties"]["next"]

    # iterates curr to next name
    def goNext(self):
        self.curr = self.getNext()

    # returns something like -0.25% slope
    def getPercentSlope(self, p1=None, p2=None):
        if(p1 == None and p2 == None):
            p1 = self.curr
            p2 = self.getNext()
        return (
            100 * (self._getElevation(p2) - self._getElevation(p1))
            / (self.getDistance(p1, p2))
        )
    # gets turning radius of next segment in feet
    def getRadius(self, p1=None):
        if(p1 == None):
            p1 = self.curr
        if("radius" in self._getPoint(p1)["properties"]):
            return self._getPoint(p1)["properties"]["radius"]
        return float("inf")
    
    # gets distance in feet from A to B and supports paths
    def getDistance(self, p1, p2):
        distance = 0
        dest = p2
        while self.getNext(p1) != dest:
            distance += self._getDirectDistance(p1, p2)
            p1 = p2
            p2 = self.getNext(p2)
        return distance + self._getDirectDistance(p1, p2)

    # private functions you shouldn't have to use
    def _getPoint(self, p1):
        return self.track["features"][self.name[p1]]

    def _getCoords(self, p1):
        return (
            self._getPoint(p1)["geometry"]["coordinates"][1],
            self._getPoint(p1)["geometry"]["coordinates"][0]
        )

    def _getElevation(self, p1):
        return self._getPoint(p1)["properties"]["elevation"]

    def _getDirectDistance(self, p1, p2):
        lat1, lon1 = self._getCoords(p1)
        lat2, lon2 = self._getCoords(p2)
        x = 288200 * (lon2 - lon1)
        y = 364000 * (lat2 - lat1)
        d = math.sqrt(x * x + y * y)
        if("radius" in self._getPoint(p1)["properties"]):
            r = self.getRadius(p1)
            return 2*r*math.asin(d/(2*r))
        return d
    

t = Track("dynamic")
t.setForks("left", "left", "left")

while t.getNext(t.getCurr()) != "S0":
    print(t.getCurr())
    t.goNext()
print(t.getCurr())
t.goNext()

print("shortest track length: " + str(t.getDistance("S0", "S0"))) #
t.pitNext()
print("above length with pit lap: " + str(t.getDistance("S0", "S0"))) # this inherently 2 laps to make it to the finish line after a pit
t.setForks("right", "right", "right")
print("longest track length: " + str(t.getDistance("S0", "S0")/5280))
