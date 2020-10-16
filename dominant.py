import sys, os, time
import networkx as nx
import numpy as np
from itertools import chain, combinations


def create_node_edges(graph):
    node_2_edge = dict()
    for node in graph.nodes:
        node_2_edge[node] = []

    for edge in graph.edges:
        origin = edge[0]
        destination = edge[1]
        node_2_edge[origin].append(destination)
        node_2_edge[destination].append(origin)

    return node_2_edge

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def check_is_dominant(subnodes, node_2_edges):

    reachable = dict()
    graph_nodes = list(node_2_edges.keys())
    need_to_visit = len(graph_nodes) - 1
    for node in graph_nodes:
        reachable[node] = 0

    for node in subnodes:
        destinations = node_2_edges[node]
        for destination in destinations:
            if reachable[destination] == 0:
                reachable[destination] = 1
                need_to_visit -= 1

    return False if need_to_visit > 0 else True


global counter = 0

def dominant(graph):
    """
        A Faire:         
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

    """

    print(" [x] Graph number", counter)
    counter += 1
    smallest_comb_size = np.inf
    smallest_comb = None
    node_2_edges = create_node_edges(graph)
    
    #print(" [.] Nodes 2 edges ", node_2_edges)
   
    node_combinations = powerset(graph.nodes)

    for node_comb in node_combinations:
        comb_size = len(node_comb)
        if comb_size > smallest_comb_size: # there's no need to test because it can't update smallest_comb
            break

        if check_is_dominant(node_comb, node_2_edges):
            if comb_size < smallest_comb_size:
                smallest_comb_size = comb_size
                smallest_comb = node_comb

    #print(" [.] Smallest combination: ", smallest_comb)
    #print(" [.] Smallest combination size: ", smallest_comb_size)
    return smallest_comb

#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__=="__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])
    
    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
	    print(input_dir, "doesn't exist")
	    exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
	    print(input_dir, "doesn't exist")
	    exit()       
	
    # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))             
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    for graph_filename in sorted(os.listdir(input_dir)):
        # importer le graphe
        g = nx.read_adjlist(os.path.join(input_dir, graph_filename))
        
        # calcul du dominant
        D = sorted(dominant(g), key=lambda x: int(x))

        # ajout au rapport
        output_file.write(graph_filename)
        for node in D:
            output_file.write(' {}'.format(node))
        output_file.write('\n')
        
    output_file.close()
