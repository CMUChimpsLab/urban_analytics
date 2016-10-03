from geopy.distance import vincenty
areaCoordinateList =[
        (40.441697, -80.001036),
        (40.441980, -79.962566),
        (40.439136, -79.989892),
        (40.429326, -79.972877),
        (40.446842, -80.005434),
        (40.446751, -80.015612),
        (40.454168, -79.982482),
        (40.443425, -79.943467),
        (40.432828, -79.964569),
        (40.433096, -80.004640),
        (40.467497, -79.960566),
        (40.452886, -79.931401),
        (40.458851, -79.904262),
        (40.407686, -79.916811),
        (40.413318, -80.022684),
        (40.374081, -80.047491),
        (40.443431, -79.968571)
    ]
areaNameList = [
    "downtown",
    "oakland",
    "console energy center",
    "southside",
    "pnc park",
    "heinz field",
    "strip district",
    "cmu",
    "pitts tech center",
    "station square",
    "lawrenceville",
    "shadyside",
    "homewood",
    "homestead waterfront",
    "beechview",
    "Mt Lebanon",
    "terrace village",
]



def getClusterIndex(coordinate):
    distance = 1000000
    index = -1
    for i in range(len(areaCoordinateList)):
        tmp = vincenty(areaCoordinateList[i], coordinate).km
        if tmp>1:
            continue
        if vincenty(areaCoordinateList[i], coordinate).km<distance:
            distance = vincenty(areaCoordinateList[i], coordinate).km
            index = i
    return index

def getClusterName(index):
    return areaNameList[index]
