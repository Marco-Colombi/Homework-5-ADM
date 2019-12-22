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
sys.setrecursionlimit(100000)

#Main function for task 4
def Function_4(G, lat, lon):
    H = int(input('Enter the starting node: ', ))
    p = list(map(int, input('Which are the nodes that you want to visit? : ', ).split()))
    res = Shortest_Route(H, p, G)
    #Not finding a walk
    if res == 'NA':
        print('Not possible!')
        return
    #Finding a walk
    else:
        complete_walk = res[0]
        tot_dist = res[1]
    print('The total distance of the walk is :', tot_dist)
    #Visualization Part
    plt.figure(figsize = (20, 18))
    figsize = (32, 67)
    #taking the latitude and the longitude of the complete walk
    latitudes = [lat[i-1] for i in complete_walk]
    longitudes = [lon[i-1] for i in complete_walk]
    #creating the map
    m = Basemap(projection = 'merc', llcrnrlon = min(latitudes) - 0.1, llcrnrlat = min(longitudes) - 0.1,
            urcrnrlon = max(latitudes) + 0.1, urcrnrlat = max(longitudes) + 0.1, lat_ts = 0,
            resolution = 'i') 
    m.drawparallels([min(latitudes) - 0.1, max(latitudes) + 0.1])
    m.drawmeridians([min(longitudes) - 0.1, max(longitudes) +0.1])
    #plotting the path
    x, y = m(latitudes, longitudes)
    m.plot(x, y, '->', markersize = 1, linewidth = 2, color = 'white', markerfacecolor = 'white')
    #plotting the destination nodes
    latitudes = [lat[i-1] for i in p]
    longitudes = [lon[i-1] for i in p]
    x, y = m(latitudes, longitudes) 
    m.plot(x, y, 'v', markersize = 15, linewidth = 10, color = 'violet', markerfacecolor = 'violet')
    for i in p:
        x, y = m(lat[i-1], lon[i-1])
        plt.annotate(str(i), xy=(x, y), xycoords='data', xytext=(x, y), textcoords='data', size = 15,
                     color = 'cyan')
    #plotting the starting node
    latitudes = [lat[H-1]]
    longitudes = [lon[H-1]]
    x, y = m(latitudes, longitudes)
    m.plot(x, y, '*', markersize = 15, linewidth = 10, color = 'gold', markerfacecolor = 'gold', label = 'start')
    #more fancy things for the map
    m.drawcoastlines()
    m.drawmapboundary(fill_color = '#A6CAE0', linewidth = 0)
    m.fillcontinents(color = 'black', alpha = 0.7, lake_color = 'aqua')
    m.drawstates(color = 'black')
    m.drawcountries(color = 'black')
    plt.title("4. Shortest Route with Dijkstra")
    plt.show()
 
#Obtaining the Shortest Route
def Shortest_Route(H, p, G):
    copy = p[:]
    start_node = H #this is the starting point
    tot_dist = 0 #saving the total distance
    end = copy[-1]
    complete_walk = []
    #The two below paramters allow us to know 
    #at which point (in the middle or at the end) 
    #of the walk we are
    counter = 1
    l = len(p)
    #with this loop we will have the unordered 
    #complete route and its distance using Dijkstra
    while copy:
        result = Unordered_Dijkstra(start_node, copy, end, counter, l, G) 
        #In the case it's not possible finding a Walk which passes through all the nodes
        if result == 'NA':
            return result
        else:
            complete_walk.extend(result[0])
            tot_dist += result[1]
            start_node = result[2]  #the reached node becomes the start_node
            print('The', counter, 'node to visit is:', start_node)
            #Removing the reached node from the walk
            copy.remove(start_node)
            counter += 1
    return complete_walk, tot_dist

#Dijstrka for unordered walk
def Unordered_Dijkstra(start, walk_copy, end, counter, length, G):
    flag = False  #it allows us to know if the nodes are reachable from the start
    n = len(list(G.vertList.keys()))
    distances = [math.inf] * n #distances from the start
    distances[start - 1] = 0 
    visited = bitarray(n)
    visited.setall(0)      # a bit = 1 if a node was visited
    prev_node = [None] * n #knowing the node which precedes another node
    pq = []  #Priority queue : mantaining the nodes with the min dist from the start
    heapq.heappush(pq,(distances[start - 1], start))
    while pq:
        node_id = heapq.heappop(pq)[1] #taking with the min distance from the start
        #if the node is in the walk:
        if node_id in walk_copy: 
            #and it's the end and we are at the 
            #walk's end we break the loop
            if node_id == end and counter == length:
                flag = True
                break
            #or it's not the end and we are not at the
            #walk's end we break the loop
            elif node_id != end and counter < length:
                flag = True
                break
        visited[node_id - 1] = 1 #taking the node as visited
        node = G.getVertex(str(node_id)) #taking the node and his neighbors
        neighbours = node.getConnections()
        for nbr in neighbours:
            nbr_id = int(nbr.getId())
            if visited[nbr_id - 1] == 0: #checking if the node isn't visited
                weight = int(node.getWeight(nbr)) 
                #Checking if we found a shortest path for this neighbour
                if distances[nbr_id - 1] > distances[node_id - 1] + weight: 
                    distances[nbr_id - 1] = distances[node_id - 1] + weight
                    prev_node[nbr_id - 1] = node_id - 1 #changing the previous node
                    heapq.heappush(pq,(distances[nbr_id - 1], nbr_id)) #pushing the node in the heap
                    
    #If we reached a node in the walk we take the walk
    #from the start to the reached node
    if flag == True:  
        walk = [node_id]
        Return_Walk(prev_node, walk, node_id, start)
        walk.reverse()
        return walk, distances[node_id - 1], node_id
    else:
        return "NA"
 
#Obtaining the walk from the starting to
#the ending node using the prev_list  
def Return_Walk(delta, walk, node, start):
    prev = delta[node - 1] + 1 
    walk.append(prev)
    if prev == start:
        return walk
    else:
        new_node = delta[node - 1] + 1
        return Return_Walk(delta, walk, new_node, start)