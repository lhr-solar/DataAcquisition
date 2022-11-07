import json
import math


class Track:

    track = 0
    curr = "S0"
    name = {}
    pit = 0

    def __init__(self, trackName):
        with open("app/track/track.geojson", "r") as f:
            self.track = json.load(f)
        for i in range(len(self.track["features"])):
            self.name.update({self.track["features"][i]["properties"]["name"]: i})

    def setPit(self, pit):
        self.pit = pit

    def getCurr(self):
        return self.curr

    def getNext(self, p1):
        return self._getPoint(p1)["properties"]["next"][self.pit]

    def goNext(self):
        self.curr = self.getNext(self.curr)

    def getPercentSlope(self, p1, p2):
        return (
            100 * (self._getElevation(p2) - self._getElevation(p1))
            / (self.getDistance(p1, p2))
        )

    def getDistance(self, p1, p2):
        distance = 0
        while p2 != self.getNext(p1):
            distance += self._getDirectDistance(p1, p2)
            p1 = p2
            p2 = self.getNext(p2)
        return distance + self._getDirectDistance(p1, p2)

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
        return math.sqrt(x * x + y * y)


t = Track("alpha")
print(t.getDistance("S1", "S3"))
print(t.getPercentSlope("S1", "S2"))
