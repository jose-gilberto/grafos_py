# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import networkx as nx

class Grafo:
    """Representação de um grafo simples utilizando mapas adjascentes."""

    # --- Classe interna do Vértice ---
    class Vertice:
        """Estrutura de vértice padrão para um grafo."""
        __slots__ = '_elemento', '_visitado'

        def __init__(self, e):
            """Nunca chame o construtor diretamente.
            Utilize a função do Grafo: inserir_vertice(e)."""
            self._visitado = False
            self._elemento = e

        def elemento(self):
            return self._elemento

        def __str__(self):
            return str(self._elemento)

        def __hash__(self):
            # Vai permitir que o vertice se comporte como um map/set (conjunto)
            return hash(id(self))

    # --- Classe interna da Aresta ---
    class Aresta:
        """Estrutura de aresta padrão para um grafo."""
        __slots__ = '_origem', '_destino', '_peso'

        def __init__(self, origem, destino, peso):
            """Nunca chame o construtor diretamente.
            Utilize a função do Grafo: inserir_aresta(o, d, e)."""
            self._origem = origem
            self._destino = destino
            self._peso = peso

        def vertices(self):
            """Retorna a tupla (o, d) dos vértices de origem e destino."""
            return (self._origem, self._destino)

        def oposto(self, v):
            """Retorna o vétice que esta oposto ao v desta aresta."""
            return self._destino if v is self._origem else self._origem

        def peso(self):
            """Retorna o peso associado a essa aresta."""
            return self._peso

        def __str__(self):
            """Retorna o """
            return str(self._origem) + str(self._destino) + ';' + str(self._peso)

        def __hash__(self):
            # Vai permitir que a aresta se comporte como um map/set
            return hash((self._origem, self._destino))

    def __init__(self, direcionado=False):
        """ Cria um grafo vazio (sem direção, por padrão). Um grafo somente é
        direcionado se a opcao direcionado for atribuida como True."""
        self._saida = {}
        # Somente cria um segundo mapa para um grafo direcionado
        # Utilizar um alias para não direcionados
        self._entrada = {} if direcionado else self._saida

    def e_direcionado(self):
        """Retorna True se o grafo for direcionado.False caso contrario"""
        # Direcionado se os mapas forem distintos
        return self._entrada is not self._saida

    def num_vertices(self):
        """Retorna o numero de vertices do grafo."""
        return len(self._saida)

    def vertices(self):
        """Retorna uma iteração de todos os vértices do grafo."""
        return self._saida.keys()

    def num_arestas(self):
        """Retorna o numero de arestas do grafo."""
        total = sum(len(self._saida[v]) for v in self._saida)
        # Para grafos sem direção, não contar as arestas duplas
        return total if self.e_direcionado() else total // 2

    def arestas(self):
        """Retorna o conjunto de todas as arestas do grafo."""
        resultado = set()  # evita arestas clones
        for map_secundario in self._saida.values():
            resultado.update(map_secundario.values())
        return resultado

    def aresta(self, u, v):
        """Retorna a aresta de u até v, ou None caso não sejam adjascentes."""
        return self._saida[u].get(v)  # Retorna None caso não adjascente

    def grau(self, v, saida=True):
        """Retorna o número de arestas (de saída) incidente no vértice v no
        Grafo. Se o Grafo for direcionado, há um parâmetro opcional utilizado
        para contar as arestas de entrada."""
        adj = self._saida if saida else self._entrada
        return len(adj[v])

    def arestas_incidentes(self, v, saida=True):
        """Retorna todas as arestas incidentes (de saída) no vértice v do Grafo
        Se o Grafo for direcionado, utilize o parâmetro opcional para requerir
        os vértices de entrada."""
        adj = self._saida if saida else self._entrada
        for aresta in adj[v].values():
            yield aresta

    def inserir_vertice(self, x=None):
        """Insere e retorna um vértice de elemento x."""
        v = self.Vertice(x)
        self._saida[v] = {}
        if self.e_direcionado():
            # necessita um mapa distinto para arestas de saida
            self._entrada[v] = {}
        return v

    def inserir_aresta(self, u, v, x=None):
        """Insere e retorna uma aresta de u até v com elemento auxiliar x."""
        a = self.Aresta(u, v, x)
        self._saida[u][v] = a
        self._entrada[v][u] = a
        return a

    # TODO: implementar método para leitura de grafos em txt
    @staticmethod
    def importar_txt(caminho=None, direcionado=False):
        try:
            if caminho is not None:
                arquivo = open(caminho, 'r')
                elementos_grafo = []
                for linha in arquivo:
                    elementos_grafo.append(linha.split('=')[1].replace(
                        '{', '').replace('}', '').replace('\n', '').split(','))
                print(elementos_grafo)
            else:
                print("O caminho passado não pode ser vazio")
        except:
            print("Um erro ocorreu ao tentar acessar o arquivo.")
        finally:
            arquivo.close()


# Grafo.importar_txt(caminho="./grafo.txt")

# Criando grafo
grafo_exemplo = Grafo()
# Inserindo vertices
v1 = grafo_exemplo.inserir_vertice('a')
v2 = grafo_exemplo.inserir_vertice('b')
v3 = grafo_exemplo.inserir_vertice('c')
v4 = grafo_exemplo.inserir_vertice('d')
v5 = grafo_exemplo.inserir_vertice('e')
v6 = grafo_exemplo.inserir_vertice('f')
# Inserindo arestas
grafo_exemplo.inserir_aresta(v1, v2)
grafo_exemplo.inserir_aresta(v1, v3)
grafo_exemplo.inserir_aresta(v3, v4)
grafo_exemplo.inserir_aresta(v2, v4)

G = nx.Graph()

for vertice in grafo_exemplo.vertices():
   G.add_node(vertice.elemento())

for aresta in grafo_exemplo.arestas():
    origem, destino = aresta.vertices()
    G.add_edge(origem.elemento(), destino.elemento())

print(G.number_of_nodes())
#G = nx.petersen_graph()

#plt.subplot(121)
nx.draw(G, with_labels = True)
#plt.subplot(122)
#nx.draw_shell(G, with_labels=True, font_weight='bold')
plt.show()


