import geojson
import requests


def getElevation(lat, lon):
    response = requests.get(
        "https://nationalmap.gov/epqs/pqs.php?x="
        + str(lon)
        + "&y="
        + str(lat)
        + "&units=Feet&output=json"
    ).json()
    return response["USGS_Elevation_Point_Query_Service"]["Elevation_Query"]["Elevation"]


def updateElevation(trackName):
    with open("app/track/" + trackName + ".geojson", "r") as f:
        track = geojson.load(f)
    for feature in track["features"]:
        elevation = getElevation(
            feature["geometry"]["coordinates"][1], feature["geometry"]["coordinates"][0]
        )
        print(elevation)
        feature["properties"].update({"elevation": elevation})
    with open("app/track/" + trackName + ".geojson", "w") as f:
        geojson.dump(track, f, indent=4)
    print("Elevation updated.")


def updateNameNext(trackName):
    with open("app/track/" + trackName + ".geojson", "r") as f:
        track = geojson.load(f)
    for i in range(len(track["features"])):
        track["features"][i]["properties"].update({"name": "S" + str(i)})
        track["features"][i]["properties"].update({"next": "S" + str(i + 1)})
    with open("app/track/" + trackName + ".geojson", "w") as f:
        geojson.dump(track, f, indent=4)
    print("Properties updated.")


def convertPointToLineString(trackName):
    with open("app/track/" + trackName + ".geojson", "r") as f:
        track = geojson.load(f)
    line = geojson.LineString([])
    for feature in track["features"]:
        lat = feature["geometry"]["coordinates"][1]
        lon = feature["geometry"]["coordinates"][0]
        line["coordinates"].append([lon, lat])
    f = geojson.Feature(geometry=line)
    fc = geojson.FeatureCollection([f])
    with open("app/track/" + trackName + "Conv.geojson", "w") as f:
        geojson.dump(fc, f, indent=4)
    print("Conversion complete.")


updateElevation("HeartLand")
# updateNameNext("Heartland")
# convertPointToLineString("Heartland")