# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 04:43:41 2019

@author: marco
"""
#imports
import gzip
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import math
from bitarray import bitarray
import heapq
import sys
sys.setrecursionlimit(100000)

#Main function for task 3
def Function_3(G, lat, lon):  
    H = int(input('Input the starting node: ', ))
    p = list(map(int, input('Which are the nodes that you want to visit? : ').split()))
    res = Shortest_Ordered_Route(H, p, G)
    
    #Not finding a walk
    if res == 'NA':
        print('Not possible!')
        return 
    #Finding a walk
    else:
        complete_walk = res[0]
        distance = res[1]
    print('The total distance of the walk is: ', distance)
    
    #Visualization Part
    plt.figure(figsize = (20, 18))
    figsize = (32, 67)
    #taking the latitude and the longitude of the complete path
    latitudes = [lat[i-1] for i in complete_walk]
    longitudes = [lon[i-1] for i in complete_walk]
    #creating the map
    m = Basemap(projection = 'merc', llcrnrlon = min(latitudes) - 0.1, llcrnrlat = min(longitudes) - 0.1,
            urcrnrlon = max(latitudes) + 0.1, urcrnrlat=max(longitudes) + 0.1, lat_ts = 0,
            resolution = 'i', suppress_ticks=True)
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
    #plotting the starting nodes
    latitudes = [lat[H-1]]
    longitudes = [lon[H-1]]
    x, y = m(latitudes, longitudes)
    m.plot(x, y, '*', markersize = 15, linewidth = 2, color = 'gold', markerfacecolor = 'gold')
    #more fancy things for the map
    m.drawcoastlines()
    m.drawmapboundary(fill_color = '#A6CAE0', linewidth = 0)
    m.fillcontinents(color = 'black', alpha = 0.7, lake_color = 'aqua')
    m.drawstates(color = 'black')
    m.drawcountries(color = 'black')
    plt.title("3. Shortest Ordered Route with Dijkstra")
    plt.show()
    
#Finfinding the Shortest Ordered Route
def Shortest_Ordered_Route(H, p, G):
    copy = p[:]
    copy.insert(0, H)
    tot_dist = 0 #saving the total distance
    complete_walk = []
    
    #With this loop we will have the shortest ordered
    #route and its total distance using Dijkstra
    for i in range(1, len(copy)):
        result = Ordered_Dijkstra(copy[i-1], copy[i], G) 
        #In the case it's not possible finding a 
        #Walk which passes through all the nodes
        if result == 'NA':
            return 'NA'
        else:
            complete_walk.extend(result[0])
            tot_dist += result[1]
    return complete_walk, tot_dist

#Implementing Dijkstra Algorithm for ordered walk
def Ordered_Dijkstra(start, end, G):
    flag = False
    n = len(list(G.vertList.keys()))
    distances = [math.inf] * n
    distances[start - 1] = 0
    visited = bitarray(n)
    visited.setall(0) #it's equal 1 if a node was visited
    prev_node = [None] * n #knowing the node which precedes another node
    pq = [] #Priority queue
    heapq.heappush(pq,(distances[start - 1], start))
    
    while pq:
        #Taking the node with the minimum distance from the start
        node_id = heapq.heappop(pq)[1]
        if end == node_id:
            #if we have reached the destination node of
            #the path we can break the loop
            flag = True
            break
        visited[node_id - 1] = 1 #taking the node as visited
        node = G.getVertex(str(node_id)) #taking the node and his neighbors
        neighbours = node.getConnections()
        for nbr in neighbours:
            nbr_id = int(nbr.getId())
            if visited[nbr_id - 1] == 0: #checking if the node was not visited
                weight = int(node.getWeight(nbr)) 
                
                #Checking if we found a shortest path for this neighbour
                if distances[nbr_id - 1] > distances[node_id - 1] + weight:  
                    distances[nbr_id - 1] = distances[node_id - 1] + weight
                    prev_node[nbr_id - 1] = node_id - 1 
                    heapq.heappush(pq,(distances[nbr_id - 1], nbr_id))
                    
      
    #if our destination node is reachable from the starting point
    if flag == True:  
        walk = [end]
        Return_Walk(prev_node, walk, end, start)
        walk.reverse()
        return walk, distances[end - 1]
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