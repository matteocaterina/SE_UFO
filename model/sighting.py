from dataclasses import dataclass
import datetime

@dataclass
class Sighting:
    id: int
    s_datetime: datetime.datetime
    city: str
    state: str
    country: str
    shape: str
    duration: float
    duration_hm: str
    comments: str
    date_posted: datetime.datetime
    latitude: float
    longitude: float

    def __str__(self):
        return f"{self.id}"
    def __repr__(self):
        return f"{self.id}"