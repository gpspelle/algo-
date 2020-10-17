import sys, os, time
import networkx as nx
import numpy as np
from itertools import chain, combinations

class Printer():
    """Print things to stdout on one line dynamically"""
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()

def brute_force_create_node_edges(graph):
    node_2_edges = dict()
    for node in graph.nodes:
        node_2_edges[node] = [node]

    for edge in graph.edges:
        origin = edge[0]
        destination = edge[1]
        node_2_edges[origin].append(destination)
        node_2_edges[destination].append(origin)

    return node_2_edges

def create_node_edges(graph):
    node_2_edges = dict()
    node_2_edges_ = dict()
    for node in graph.nodes:
        node_2_edges[node] = [node]
        node_2_edges_[node] = [node]

    for edge in graph.edges:
        origin = edge[0]
        destination = edge[1]
        node_2_edges[origin].append(destination)
        node_2_edges[destination].append(origin)
        node_2_edges_[origin].append(destination)
        node_2_edges_[destination].append(origin)

    for node0 in node_2_edges.keys():
        for node1 in node_2_edges.keys():
            if node0 == node1:
                continue

            if node0 in node_2_edges_ and node1 in node_2_edges_:
                if set(node_2_edges[node1]) <= set(node_2_edges[node0]):
                    node_2_edges_.pop(node1)

    return node_2_edges_


def improve_answer(best_nodes, node_2_edges, start, end):

    if start >= end:
        return best_nodes

    middle = (start + end) // 2
    for comb in combinations(best_nodes, middle):
        if faster_check_is_dominant(comb, node_2_edges):
            return comb

    return improve_answer(best_nodes, node_2_edges, middle+1, end)


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


#def check_is_dominant(subnodes, node_2_edges):
#    global graph_nodes_len
#    global graph_nodes 
#
#    reachable = dict()
#    for node in graph_nodes:
#        reachable[node] = 0
#
#    visited = 0
#    for node in subnodes:
#        if visited == graph_nodes_len:
#            break
#
#        destinations = node_2_edges[node]
#        for destination in destinations:
#            if reachable[destination] == 0:
#                reachable[destination] = 1
#                visited += 1
#
#    return False if visited != graph_nodes_len  else True


def faster_check_is_dominant(subnodes, node_2_edges):
    all_destinations = set()
    for node in subnodes:
        all_destinations.update(set(node_2_edges[node]))
        
    return False if len(all_destinations) != graph_nodes_len else True


graph_nodes_len = 0

def get_most_central(node_2_edges, found_nodes):

    biggest = -np.inf
    central_node = None

    for node in node_2_edges.keys():
        node_neighbors = set(node_2_edges[node])

        not_found = node_neighbors.difference(found_nodes)
        size = len(not_found)

        if size > biggest:
            central_node = node
            biggest = size

    return node_2_edges.pop(central_node), central_node


#def stupid_greedy_dominant(graph):
#    """
#        A Faire:         
#        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
#        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g
#
#        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html
#
#    """
#    global graph_nodes_len
#
#    graph_nodes = graph.nodes
#    graph_nodes_len = len(graph_nodes)
#    found_nodes = set()
#    best_nodes = []
#
#    node_2_edges = create_node_edges(graph)
#
#    while len(found_nodes) < graph_nodes_len:
#        best_node_neighbors, central_node = get_most_central(node_2_edges)
#        found_nodes.update(best_node_neighbors)
#        best_nodes.append(central_node)
#
#    return best_nodes

#counter = 0
def dominant(graph):
    """
        A Faire:         
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

    """
    global graph_nodes_len
    #global counter

    #print(" [x] Graph number", counter)
    #counter += 1
    graph_nodes_len = len(graph.nodes)

    if graph_nodes_len <= 10:
        return dominant_brute_force(graph)

    found_nodes = set()
    best_nodes = []

    node_2_edges = create_node_edges(graph)

    while len(found_nodes) < graph_nodes_len:
        best_node_neighbors, central_node = get_most_central(node_2_edges, found_nodes)
        found_nodes.update(best_node_neighbors)
        best_nodes.append(central_node)

    #print(" [.] Found: ", best_nodes)
    #print(" [.] Found: ", len(best_nodes))
    if len(best_nodes) <= 6:
        return dominant_brute_force(graph) # okay, found a small answer, let's try to improve it with bruteforce
    elif len(best_nodes) >= 30:
        return best_nodes

    node_2_edges = brute_force_create_node_edges(graph)

    #print(" [.] Binary search size: ", len(best_nodes))
    #print(" [.] Best node size before: ", len(best_nodes), end='')
    best_nodes = improve_answer(best_nodes, node_2_edges, 0, len(best_nodes)) 
    #print(" - Best node size after: ", len(best_nodes))

    return best_nodes


#counter = 0
def dominant_brute_force(graph):
    """
        A Faire:         
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

    """

    global graph_nodes_len
    #global counter

    #print(" [x] Graph number", counter)
    #counter += 1

    smallest_comb_size = np.inf
    smallest_comb = []

    node_2_edges = brute_force_create_node_edges(graph)
    
    graph_nodes_len = len(graph.nodes)

    #print(" [.] Nodes 2 edges ", node_2_edges)
    #print(" Number of nodes: ", graph_nodes_len)
   
    node_combinations = powerset(graph.nodes)
    total_combinations = 2 ** graph_nodes_len

    #print(" [.] Power set size: ", total_combinations)

    #it = 0
    for node_comb in node_combinations:
        comb_size = len(node_comb)
        #output = " [x] Try number #" + str(it) + " of #" + str(total_combinations) + ". Best result: " + str(smallest_comb_size) + " and Combination size: " + str(comb_size) + "."
        #it += 1
        #Printer(output)

        if comb_size >= smallest_comb_size: # there's no need to test because it can't update smallest_comb
            break

        if faster_check_is_dominant(node_comb, node_2_edges):
            if comb_size < smallest_comb_size:
                smallest_comb_size = comb_size
                smallest_comb = node_comb

    #print()
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
