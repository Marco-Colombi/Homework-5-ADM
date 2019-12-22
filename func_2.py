# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 04:41:45 2019

@author: marco
"""
#imports
import gzip
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import math
from bitarray import bitarray
import pandas as pd
import heapq
import time
import sys
import networkx as nx
sys.setrecursionlimit(100000)

from collections import defaultdict

def make_set(vertice,parent,rank):
    parent[vertice] = vertice
    rank[vertice] = 0
# A utility function to find set of an element i
# (uses path compression technique)
def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

# A function that does union of two sets of x and y
# (uses union by rank)
def union( parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)

    # Attach smaller rank tree under root of high rank tree
    # (Union by Rank)
    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    #If ranks are same, then make one as root and increment
    # its rank by one
    else :
        parent[yroot] = xroot
        rank[xroot] += 1

# The main function to construct MST using Kruskal's algorithm
def KruskalMST(verts,edges):
    verts = [int(x) for x in verts]
    verts.sort()
    edges = sorted(edges,key=lambda item: item[2])

     
    minimum_spanning_tree = []
   

    #Step 1:  Sort all the edges in non-decreasing order of their
    # weight.  If we are not allowed to change the given graph, we
    # can create a copy of graph
    
    #print self.graph

    parent = [0]*(len(verts)+1); 
    
    rank = [0]*(len(verts)+1);

    
    for i in range(len(verts)):
        make_set(i,parent,rank)
   
        #edges = sorted(dist_file,key=lambda item: item[2]) 
    
    
    for edge in edges:
        vertice1, vertice2,weight = edge
        if find(parent,verts.index(vertice1)) != find(parent,verts.index(vertice2)):
            union(parent,rank,verts.index(vertice1),verts.index(vertice2) )
            minimum_spanning_tree.append(edge)

    return minimum_spanning_tree

def new_graph(nodes):
    #this function create the new graph with the considered nodes
    red_g = []
    nodes = [str(x) for x in nodes]
    for n1 in nodes:
        list_of_nodes = [a.id for a in list(g.getVertex(n1).getConnections())]

        for i in range(len(list_of_nodes)):
            if list_of_nodes[i] in nodes:
                new_edge = [n1, list_of_nodes[i], list((g.getVertex(n1).connectedTo).values())[i]]
                red_g.append(new_edge)
    
    red_g = [[int(x) for x in lis] for lis in red_g ]
    
    
    #visualization
    
    G = nx.Graph()
    for link in red_g:
        G.add_edge(str(link[0]), str(link[1]), weight=link[2])


    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge,
                           width=6)
    nx.draw_networkx_edges(G, pos, edgelist=esmall,
                           width=6, alpha=0.5, edge_color='b', style='dashed')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    plt.axis('off')
    plt.show()
    
#Kruskal works both on connected and not connected graph
#in this case we analize the results of an input of nodes and an out that can be a connected graph
#so roads which connect all the cities passing just in those cities
#and the case where there can't be a connection through the cities using just those cities

def Function_2(g):
    inp=input('Give me a set of nodes (separated by space): ')
    nodes=list(map(int, inp.split()))
    return KruskalMST(nodes,g)


