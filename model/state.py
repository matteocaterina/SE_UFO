from dataclasses import dataclass

@dataclass
class State:
    id: str
    name: str
    capital: str
    lat: float
    lng: float
    area:float
    population: float
    neighbors: list

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __hash__(self):
        return hash(self.id)