# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 12:11:40 2019

@author: marco
"""
import gzip
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import math
from bitarray import bitarray
import heapq

def Function_1(G, col, lat, lon):  
    v = int(input('Enter a node: '))  # the initial node
    d = int(input('Enter a distance threshold: '))  #the distance threshold
    neighbours = find_neighbours(v, d, G)
    print(neighbours)
    #Visualization Part
    plt.figure(figsize = (20, 18))
    figsize = (32, 67)
    #taking the latitude and the longitude of the complete path
    latitudes = [lat[i-1] for i in neighbours]
    longitudes = [lon[i-1] for i in neighbours]
    #creating the map
    m = Basemap(projection = 'merc', llcrnrlon = min(latitudes) - 0.001, llcrnrlat = min(longitudes) - 0.001,
            urcrnrlon = max(latitudes) + 0.001, urcrnrlat = max(longitudes) +0.001, lat_ts = 0,
            resolution = 'i', suppress_ticks=True)
    #plotting the path
    x, y = m(latitudes, longitudes)
    m.plot(x, y, '.', markersize = 1, linewidth = 2, color = col, markerfacecolor = col)
    #plotting the starting nodes
    latitudes = [lat[v-1]]
    longitudes = [lon[v-1]]
    x, y = m(latitudes, longitudes)
    m.plot(x, y, '*', markersize = 5, linewidth = 2, color = 'gold', markerfacecolor = 'gold')
    #more fancy things for the map
    m.drawcoastlines()
    m.drawmapboundary(fill_color = '#A6CAE0', linewidth = 0)
    m.fillcontinents(color = 'black', alpha = 0.7, lake_color = 'aqua')
    m.drawstates(color = 'black')
    m.drawcountries(color = 'black')
    plt.title("1. Find Neighbours with Dijkstra")
    plt.show()

#Implementing Dijkstra Algorithm for ordered walk
def find_neighbours(v, d, g):
    # The algorithm for this part is BFS with a distance
    # The visited state is a list that: if visit_state[i] = True it means the i-th node was visited
    # The dist is an array that will contain the distances of all visited nodes from the initial node
    visit_state = [False]*(len(list(G.vertList.keys()))+1) 
    dist = [0]*(len(list(G.vertList.keys()))+1) 
    visited = set() 
    queue = []
    queue.append(v)
    visit_state[v] = True
    visedge = [] # To save the edges of neighbors(not necessary)
    while queue:
        s = queue.pop()
        
        n =[a.id for a in list(g.getVertex(str(s)).getConnections())]# n is the neighbors of s
        n = [int(x) for x in n]
        
        for i in range(len(n)):
            
            if visit_state[i] == False:
                weight =int(list((g.getVertex(str(s)).connectedTo).values())[i])
                temp = weight + dist[s]
                if temp <= d:
                    queue.append(n[i])
                    visit_state[n[i]]=True
                    visited.add(n[i])
                    dist[n[i]]=temp
                    visedge.append((s,n[i]))
    return visited