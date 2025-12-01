from dataclasses import dataclass
from model.object import Object

# classe che mette in relazione due oggetti
@dataclass
class Connessione:
    o1 : Object
    o2 : Object
    peso : int