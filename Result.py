class Result:
    id: str
    day: dict

    def __init__(self, id, day):
        self.id = id
        self.day = day

    def to_dict(self):
        return {"id": self.id, "day": self.day}
