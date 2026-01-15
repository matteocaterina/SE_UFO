from database.dao import DAO
import networkx as nx
from geopy import distance

class Model:
    def __init__(self):
        self.lista_anni = []
        self.lista_shapes = []
        self.lista_states = []

        self.G = nx.Graph()
        self._nodes = []
        self._edges = []
        self.id_map = {}
        self.lista_connessioni = []

        self.load_anni()
        self.load_shapes()
        self.load_states()

        self.peso_ottimo = 0
        self.percorso_best = []


    def load_anni(self):
        self.lista_anni = DAO.get_anni()
        return self.lista_anni

    def load_shapes(self):
        self.lista_shapes = DAO.get_shapes()
        return self.lista_shapes

    def load_states(self):
        self.lista_states = DAO.get_states()
        return self.lista_states

    def crea_grafo(self, shape, year):
        for state in self.lista_states:
            self._nodes.append(state)

        for state in self.lista_states:
            self.id_map[state.id] = state

        self.G.add_nodes_from(self._nodes)

        self.lista_connessioni = DAO.get_archi(shape,year)
        for s1,s2,n in self.lista_connessioni:
            self._edges.append((self.id_map[s1], self.id_map[s2],n))

        self.G.add_weighted_edges_from(self._edges)

    def calcola_peso(self):
        result = []
        for stato in self.G.nodes():
            sum = 0
            for v in self.G.neighbors(stato):
                sum += self.G[stato][v]['weight']
            result.append((stato.id, sum))
        return result

    def cammino_massimo(self):
        #archi di peso crescente
        self.peso_ottimo = 0
        self.percorso_best = []
        for stato in self.G.nodes():
            self._ricorsione([stato], [], float('-inf'))

        return self.percorso_best, self.peso_ottimo

    def _ricorsione(self, parziale, edge_parziale, last_edge_weight):
        ultimo_nodo = parziale[-1]
        vicini = self.get_vicini(ultimo_nodo, last_edge_weight)

        if len(vicini) == 0:
            peso_corrente = self.calcolaPeso(edge_parziale)
            if peso_corrente > self.peso_ottimo:
                self.peso_ottimo = peso_corrente
                self.percorso_best = edge_parziale.copy()
            return

        for v,w in vicini:
            edge_parziale.append((ultimo_nodo,v, self.G[ultimo_nodo][v]['weight']))
            parziale.append(v)

            self._ricorsione(parziale, edge_parziale, w)

            edge_parziale.pop()
            parziale.pop()


    def get_vicini(self, ultimo_nodo, last_edge_weight):
        result = []
        for v in self.G.neighbors(ultimo_nodo):
            w = self.G[ultimo_nodo][v]['weight']
            if w > last_edge_weight:
                result.append((v, w))
        return result

    def get_distance(self,nodo1, nodo2):
        return  distance.geodesic((nodo1.lat, nodo1.lng), (nodo2.lat, nodo2.lng))

    def calcolaPeso(self, edge_parziale):
        d = 0
        for e in edge_parziale:
            d += distance.geodesic((e[0].lat, e[0].lng),
                                        (e[1].lat, e[1].lng)).km
        return d







