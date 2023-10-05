import json
from NurseDto import NurseDto


def getJson(nursesDataString):
    nursesDataJson = json.loads(nursesDataString.decode("UTF-8"))
    return nursesDataJson


def getValues(nursesDataJson):
    chargeNurses = []
    actNurses = []

    startDate = nursesDataJson.get("startDate")
    day = nursesDataJson.get("day")
    maxNight = nursesDataJson.get("maxNight")
    maxNurse = nursesDataJson.get("maxNurse")
    minNurse = nursesDataJson.get("minNurse")
    # sleepingOff = nursesDataJson.get("sleepingOff")

    for chargeNurse in nursesDataJson["chargeNurses"]:
        if "off" in chargeNurse:
            tmp = []
            for date in chargeNurse["off"]:
                tmp.append(dateChange(date))
            chargeNurse["off"] = tmp
        if "rest" in chargeNurse:
            tmp = []
            for date in chargeNurse["rest"]:
                tmp.append(dateChange(date))
            chargeNurse["rest"] = tmp
        chargeNurses.append(chargeNurse)

    for actNurse in nursesDataJson["actNurses"]:
        if "off" in actNurse:
            tmp = []
            for date in actNurse["off"]:
                tmp.append(dateChange(date))
            actNurse["off"] = tmp
        if "rest" in actNurse:
            tmp = []
            for date in actNurse["rest"]:
                tmp.append(dateChange(date))
            actNurse["rest"] = tmp
        actNurses.append(actNurse)

    result = NurseDto(
        chargeNurses, actNurses, day, maxNight, maxNurse, minNurse, startDate
    )
    return result


def dateChange(date):
    data = date.split("-")
    return int(data[2])
