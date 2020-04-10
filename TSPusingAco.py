import numpy as np
import pandas as pd
from numpy import inf
from threading import Thread
import time
from random import randrange
import copy
from math import radians,sin,cos,atan2,sqrt
import timeit

 
cities=pd.read_csv('worldcities.csv',decimal=".")
indCities=cities.loc[cities['country'] == 'India']
indiaCities=indCities.sample(50)    #getting 50 citites from the file
x=indiaCities['lat']
y=indiaCities['lng']
DD = list(zip(x,y))
citiesarr=[]     #array for distance between the cities
R=6373.0

for i in range(len(DD)):
    lat1=radians(DD[i][0])      #converting the degree to radians
    lng1=radians(DD[i][1])
    citiesarr.append([])
    for j in range(len(DD)):
        lat2=radians(DD[j][0])
        lng2=radians(DD[j][1])
        dlon=lng2-lng1
        dlat=lat2   -lat1
        a=sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2     #calculating distance between two cities from latitude and longitude
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        citiesarr[i].append(c*R)

class ant:
    def __init__(self,n):
        self.city=[i for i in range(n)]      #list of cities yet to be visited
        self.tabu=[]              #list of visited cities

    def retVis(self):
        return tabu

class antthread(Thread):         #running the multiple ant program in parallel
    def __init__(self, n):
        Thread.__init__(self)
        self.n=n
    
    def run(self):
        antrun(n)

def antrun(n):            #function for the ant to visit the cities
    a=ant(n)
    current=randrange(cities)
    for k in range(n-1):
    
        c_feature=np.zeros(n)           #array for combined features
        probability=np.zeros(n)         #array for probability of ant to visit next city
        temp_visibility=copy.deepcopy(visibility[current])              #creating new temporary copy of visibility of cities from current cities
        temp_pher=copy.deepcopy(pheromone[current])                     #creating new temporary copy of pheromone at various cities
        for i in range(len(temp_pher)):
            if i in a.tabu:
                temp_pher[i]=0              #excluding the cities which are visited

        p_value=np.power(temp_pher,p_factor)                #calculating the pheromone factor pheromone^alpha
        v_value=np.power(temp_visibility,v_factor)          #calculating the visibility factor visibility^beta

        c_feature=np.multiply(p_value,v_value)              #pheromone factor*visibility factor
        total=np.sum(c_feature) 
        prob=c_feature/total                                #probability=(pheromone factor*visibility factor)/total
        
        a.city.remove(current)
        a.tabu.append(current)
        maxindex=np.argmax(prob)
        pheromone[current][maxindex]=(1-evap)*pheromone[current][maxindex]+p_value[current]         #updating the pheromone value of the next city to be travelled globally
        current=maxindex

d=np.array(citiesarr)
ants=47                 #number of ants
cities=len(d)           #number of cities to be visited
m=ants
n=cities

e_rate=0.5              #evaporation rate
p_factor=1              
v_factor=2
evap=0.4
visibility=1/d  
visibility[visibility==inf]=0   #Setting the infintiy value to 0 in visibilty

pheromone=0.1*np.ones((n,n))
threads=[]    
start = timeit.default_timer()
for j in range(m):
    t=antthread(n)
    t.start()
    threads.append(t)
    for i in threads:
        i.join()
            
route=[]
dist=0
initiali=0
for i in range(n-1):                #for calculating the optimal solution
    rphero=copy.deepcopy(pheromone[i])      #temporary pheromone of the ith city
    for j in range(n):
        if j in route:
            rphero[j]=0.0
    index=np.argmax(rphero)         #index where pheromone is max
    route.append(index)             #for getting the route of optimal solution
    dist=dist+d[initiali][index]
    initiali=index
stop = timeit.default_timer()

print(dist)
print('Time: ', stop - start)