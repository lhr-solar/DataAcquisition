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
while(t.getNext(t.getCurr()) != "S0"):
    print(t.getCurr())
    t.goNext()