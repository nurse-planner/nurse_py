class NurseDto:
    startDate: str
    chargeNurses: list
    actNurses: list
    day: int
    shifts: int
    maxNight: int
    maxNurse: int
    minNurse: int
    workingYears : int

    def __init__(
        self, chrgeNurses, actNurses, day, maxNight, maxNurse, minNurse, startDate
    ):
        self.day = day
        self.maxNight = maxNight
        self.maxNurse = maxNurse
        self.minNurse = minNurse
        self.chargeNurses = chrgeNurses
        self.actNurses = actNurses
        self.startDate = startDate
        self.shifts = 3
