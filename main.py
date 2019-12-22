# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 04:20:58 2019

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
import func_1
import func_2
import func_3
import func_4
import sys
sys.setrecursionlimit(100000)

#Class for vertex object
class Vertex(object):
    
    #Constuctor of the object Node / istance Node
    def __init__(self, node_id, latitude, longitude):    
        self.id = node_id 
        self.latitude = latitude 
        self.longitude = longitude  
        self.connectedTo = {}
        self.previous = None
    
    #storing for each node its neighbours and 
    #the relative weight
    def addNeighbor(self, nbr, weight = 0):
        self.connectedTo[nbr] = weight       
        
    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])  
    
    #knowing the neighoburs of the node     
    def getConnections(self):
        return list(self.connectedTo.keys())  
    
    #returning the id of a node
    def getId(self):                                            
        return self.id
    #knowing the distance between 
    #a node and the neighbour 
    def getWeight(self, nbr):    
        return self.connectedTo[nbr]
    
    #returning positions of a node
    def getPositions(self):
        return [self.latitude, self.longitude]

#Classes representing the 3 Graphs:
#Graph with Physical distances
class Graph_physical:    
    def __init__(self):
        self.vertList = {} 
        self.numVertices = 0  
    #Adding new vertex for the graph and mapping it
    #into the dictionary of the graph
    def addVertex(self, key, latitude, longitude):
        self.numVertices = self.numVertices + 1   
        newVertex = Vertex(key, latitude, longitude) 
        self.vertList[key] = newVertex
        return newVertex 
    
    #Obtatining lat e lot of all the nodes of the graph
    def getPositions(self):
        positions = []
        for n in self.vertList:
            node = self.vertList[n]
            pos = node.getPositions()
            positions.append(pos)
        return positions
    
    #Recalling the istance related to the key 'n' in vertList
    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]  
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList
    
    #Adding an edge between two nodes
    def addEdge(self, f, t, weight = 0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], weight)
    
    #obtaining all the vertices of the graph
    def getVertices(self):
        return self.vertList.keys() 

    def __iter__(self):
        return iter(self.vertList.values())
    
#2. Graph with time Distance
class Graph_time:    
    def __init__(self):
        self.vertList = {}  
        self.numVertices = 0  

    def addVertex(self, key, latitude, longitude):
        self.numVertices = self.numVertices + 1   
        newVertex = Vertex(key, latitude, longitude) 
        self.vertList[key] = newVertex 
        return newVertex  

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]  
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, weight=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], weight)

    def getVertices(self):
        return self.vertList.keys() 

    def __iter__(self):
        return iter(self.vertList.values())

#Graph for network distance
class Graph_network:    
    def __init__(self):
        self.vertList = {}  
        self.numVertices = 0  

    def addVertex(self, key, latitude, longitude):
        self.numVertices = self.numVertices + 1  
        newVertex = Vertex(key, latitude, longitude) 
        self.vertList[key] = newVertex 
        return newVertex  

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]  
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, weight=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], weight)

    def getVertices(self):
        return list(self.vertList.keys()) 

    def __iter__(self):
        return iter(self.vertList.values())
    
#cleaning coordinates file
coord_file = []
f1 = gzip.open('USA-road-d.CAL.co.gz','rb')
coord_file = f1.readlines()
coord_file = coord_file[7:]
for i in range(len(coord_file)):
   coord_file[i] = str(coord_file[i])
   coord_file[i] = coord_file[i].replace("\\n",'')
   coord_file[i] = coord_file[i].replace("'",'')
   coord_file[i] = coord_file[i].split(' ')
   coord_file[i].remove(coord_file[i][0])  
   coord_file[i][1]= float((coord_file[i][1])[:4] + '.' + (coord_file[i][1])[4:]) 
   coord_file[i][2]= float((coord_file[i][2])[:2] + '.' + (coord_file[i][2])[2:])

#cleaning physical distance file        
dist_file = []      
f2 = gzip.open('USA-road-d.CAL.gr.gz','rb')
dist_file = f2.readlines()
dist_file = dist_file[7:]
for i in range(len(dist_file)):
    dist_file[i] = str(dist_file[i])
    dist_file[i] = dist_file[i].replace("\\n",'')
    dist_file[i] = dist_file[i].replace("'",'')
    dist_file[i] = dist_file[i].split(' ')
for i in range(len(dist_file)):
    dist_file[i].remove(dist_file[i][0])
        
    
#cleaning time distances file 
time_file = []             
f3 = gzip.open('USA-road-t.CAL.gr.gz','rb')
time_file = f3.readlines()
time_file = time_file[7:]
for i in range(len(time_file)):
    time_file[i] = str(time_file[i])
    time_file[i] = time_file[i].replace("\\n",'')
    time_file[i] = time_file[i].replace("'",'')
    time_file[i] = time_file[i].split(' ')
for i in range(len(time_file)):
    time_file[i].remove(time_file[i][0])


#Creating the Graph with physical distances        
G_physical = Graph_physical()
for city in coord_file:
    G_physical.addVertex(city[0], city[1], city[2])
for link in dist_file:
    G_physical.addEdge(link[0], link[1], weight = link[2])


#Creating the Graph with time distances
G_time = Graph_time()
for city in coord_file:
    G_time.addVertex(city[0], city[1], city[2])
for link in time_file:
    G_time.addEdge(link[0], link[1], weight = link[2])

#Creating the graph with network distances
G_network = Graph_network()
for city in coord_file:
    G_network.addVertex(city[0], city[1], city[2])
for link in dist_file:
    G_network.addEdge(link[0], link[1], weight = 1)
 
#taking all the longitudes and latitudes       
lat = []
lon = []
for city in coord_file:
    lat.append(city[1])
    lon.append(city[2])

#The four functions belows allow the user to choose
#between physical, network and time distance    
def choice_distance_1():    
    dist_choice = int(input('Choose between: \n1.Physical distance; \n2.Time distance; \n3.Network distance. \nYour choice: ', ))
    if dist_choice == 1:
        func_1.Function_1(G_physical, 'violet', lat, lon)
    elif dist_choice == 2:
        func_1.Function_1(G_time, 'white', lat, lon)
    elif dist_choice == 3:
        func_1.Function_1(G_network, 'azure', lat, lon)
    else:
        print('Please, enter a value between: 1 - 2 - 3')
        return choice_distance_1()
                 
def choice_distance_2():    
    dist_choice = int(input('Choose between: \n1.Physical distance; \n2.Time distance; \n3.Network distance. \nYour choice: ', ))
    if dist_choice == 1:
        func_2.Function_2(G_physical)
    elif dist_choice == 2:
        func_2.Function_2(G_time)
    elif dist_choice == 3:
        func_2.Function_2(G_network)
    else:
        print('Please, enter a value between: 1 - 2 - 3')
        return choice_distance_2()
                 
def choice_distance_3():    
    dist_choice = int(input('Choose between: \n1.Physical distance; \n2.Time distance; \n3.Network distance. \nYour choice: ', ))
    if dist_choice == 1:
        func_3.Function_3(G_physical, lat, lon)
    elif dist_choice == 2:
        func_3.Function_3(G_time, lat, lon)
    elif dist_choice == 3:
        func_3.Function_3(G_network, lat, lon)
    else:
        print('Please, enter a value between: 1 - 2 - 3')
        return choice_distance_3()

def choice_distance_4():
    dist_choice = int(input('Choose between: \n1.Physical distance; \n2.Time distance; \n3.Network distance. \nYour choice: ', ))
    if dist_choice == 1:
        func_4.Function_4(G_physical, lat, lon)
    elif dist_choice == 2:
        func_4.Function_4(G_time, lat, lon)
    elif dist_choice == 3:
        func_4.Function_4(G_network, lat, lon)
    else:
        print('Please, enter a value between: 1 - 2 - 3')
        return choice_distance_4()

#This function allows the user to choose which function he wants to use
def Function_to_use():
    f_choice = int(input('Choose between: \n1.Find the Neighbours!; \n2.Find the smartest Network!; \n3.Shortest Ordered Route; \n4.Shortest Route. \nYour choice: ', ))
    if f_choice == 1:
        return choice_distance_1()
    elif f_choice == 2:
        return choice_distance_2()
    elif f_choice == 3:
        return choice_distance_3()
    elif f_choice == 4:
        return choice_distance_4()
    else:
        print('Please, enter a value between: 1 - 2 - 3 - 4')
        return Function_to_use()