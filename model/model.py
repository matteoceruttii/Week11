import networkx as nx
from database.DAO import DAO
from model.connessione import Connessione


# classe Model
class Model:
    def __init__(self):
        self._objects_list = []
        self._getObjects()
        # mi posso creare anche un dizionario di Object
        self._objects_dict = {}     # è l'ID-MAP di oggetti
        for object in self._objects_list:
            self._objects_dict[object._object_id] = object

        # creo il grafo (semplice, non diretto ma pesato come richiesto in consegna)
        self._grafo = nx.Graph()


    def _getObjects(self):
        self._objects_list = DAO.readObjects()


    def buildGrafo(self):
        # NODI
        self._grafo.add_nodes_from(self._objects_list)

        # ARCHI
        #   modo 1 (usa 80k nodi x 80k nodi query SQL)
        '''for u in self._objects_list:
            for v in self._objects_list:
                DAO.readEdges(u, v)     # metodo da scrivere nel DAO'''

        #   modo 2 (usare una query sola per estrarre le connessioni)
        connessioni = DAO.readConnessioni(self._objects_dict)
        # leggo le connessioni dal DAO
        for c in connessioni:
            self._grafo.add_edge(c.o1, c.o2, peso = c.peso)


    def calcolaConnessa(self, id_nodo):
        nodo_sorgente = self._objects_dict[id_nodo]

        # MODO 1 (usando i successori)
        successori = nx.dfs_successors(self._grafo, nodo_sorgente)

        # MODO 2 (usando i predecessori) -> devo poi incrementare di uno (inserisco anche il nodo sorgente)
        predecessori = nx.dfs_predecessors(self._grafo, nodo_sorgente)

        # MODO 3 (albero di visita) -> contiene anche il nodo sorgente
        albero = nx.dfs_tree(self._grafo, nodo_sorgente)
        return len(albero.nodes)    # numero di nodi