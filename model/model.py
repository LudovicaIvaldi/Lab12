import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._bestPath = []
        self._bestScore = 0

    def buildGraph(self, country, anno):
        self._graph.clear()
        nodes = DAO.getAllRetailers(country)
        self._graph.add_nodes_from(nodes)
        print(len(self._graph.nodes))

        for n1 in self._graph.nodes:
            for n2 in self._graph.nodes:
                if n1 != n2:
                    peso = DAO.getPesi(n1, n2, anno)
                    if peso[0] > 0:
                        self._graph.add_edge(n1, n2, weight=peso[0])
        print(len(self._graph.edges))
        return len(self._graph.nodes), len(self._graph.edges)

    def calcolaVolume(self):
        volumi = {}
        for n in self._graph.nodes():
            peso = 0
            vicini = self._graph.neighbors(n)
            for vicino in vicini:
                # print(self._graph[n][vicino]["weight"])
                peso += self._graph[n][vicino]["weight"]
            volumi[n.Retailer_name] = peso
        sortato = sorted(volumi.items(), key=lambda x: x[1], reverse=True)
        return dict(sortato)

    def getPercorso(self, N):
        self._bestScore = 0
        self._bestPath = []  # voglio una lista di tuple con (n1, n2, peso), (n2, n3, peso) ...
        parziale = []
        self._ricorsione(parziale,N)
        return self._bestScore, self._bestPath

    def _ricorsione(self, parziale, N):
        # Se il percorso ha almeno un arco, deduco il nodo corrente dall'ultimo arco
        if len(parziale)==N+1 and parziale[-1]==parziale[0]:
            if self.getScore(parziale)>self._bestScore:
                self._bestScore = self.getScore(parziale)
                self._bestPath = copy.deepcopy(parziale)
        if len(parziale)==N+1:
            return
        #devo metterlo qui e non come condizione terminale se no mi lascia aperte tutte le ricorsioni
        #in cui la lughezza supera N, perchè non entra nell'if e non le chiude
        else:
            if len(parziale)==0:
                for n in self._graph.nodes:
                    parziale.append(n)
                    # print(parziale)
                    self._ricorsione(parziale, N)
                    parziale.pop()
            else:
                for n in self._graph.neighbors(parziale[-1]):
                    if n not in parziale[1:]:
                        parziale.append(n)
                        # print(parziale)
                        self._ricorsione(parziale, N)
                        parziale.pop()



    def getScore(self, parziale):
        pesoTot = 0
        for i in range(0,len(parziale)-1):
            pesoTot += self._graph[parziale[i]][parziale[i+1]]['weight']
        # print(pesoTot)
        return pesoTot


    def getPeso(self,n1,n2):
        return self._graph[n1][n2]["weight"]









