#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 参考文献

# 線分の交差判定
# https://qiita.com/wihan23/items/03efd7cd40dfec96a987

# 焼きなましについて
# https://shindannin.hatenadiary.com/entry/2021/03/06/115415


# In[2]:


#!/usr/bin/env python3

import sys
import math
import random
import time
import csv
import copy


# In[3]:


# calculate a probability for simulated annealing
def getProbability(start_time, time_limit, new_total_distance, total_distance, initial_distance):
    if (new_total_distance<total_distance):
        return 1.0
    start_temp = initial_distance*0.025;
    end_temp = initial_distance*0.0075;
    temp = start_temp + (end_temp - start_temp) * (time.time()/(start_time+time_limit))
    probability = math.exp((total_distance-new_total_distance)/temp)
    return probability


# In[4]:


# calculate a distance between the two points
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# In[5]:


# swap two points inside the route
def swapRoute(cities, tour, total_distance, first, second):
    
    new_tour = tour[:]
    new_total_distance = total_distance
    
    subtract1 = distance (cities[new_tour[first]], cities[new_tour[first+1]])
    subtract2 = distance (cities[new_tour[second]], cities[new_tour[second+1]])
    subtract3 = distance (cities[new_tour[first]], cities[new_tour[first-1]])
    subtract4 = distance (cities[new_tour[second]], cities[new_tour[second-1]])
    
    temp = new_tour[first]
    new_tour[first] = new_tour[second]
    new_tour[second] = temp
    
    add1 = distance (cities[new_tour[first]], cities[new_tour[first+1]])
    add2 = distance (cities[new_tour[second]], cities[new_tour[second+1]])
    add3 = distance (cities[new_tour[first]], cities[new_tour[first-1]])
    add4 = distance (cities[new_tour[second]], cities[new_tour[second-1]])
    
    new_total_distance -= (subtract1 + subtract2 + subtract3 + subtract4)
    new_total_distance += (add1 + add2 + add3 + add4)
    
    return new_tour, new_total_distance


# In[6]:


# checking whether x or y coordinates of two lines (created by p1&p2 and p3&p4) has an intersection
def max_min_cross(p1, p2, p3, p4):
    min_ab = min(p1, p2)
    max_ab = max(p1, p2)
    min_cd = min(p3, p4)
    max_cd = max(p3, p4)

    if min_ab > max_cd or max_ab < min_cd:
        return False

    return True


# checking whether two lines (created by p1&p2 and p3&p4 has an intersection)
def judgeCross(i, j, cities, tour):
    first = cities[tour[i]]
    second = cities[tour[j]]
    first_next = cities[tour[i+1]]
    second_next = cities[tour[j+1]]
    # x座標による判定
    if not max_min_cross(first[0], first_next[0], second[0], second_next[0]):
        return False

    # y座標による判定
    if not max_min_cross(first[1], first_next[1], second[1], second_next[1]):
        return False

    tc1 = (first[0] - first_next[0]) * (second[1] - first[1]) + (first[1] - first_next[1]) * (first[0] - second[0])
    tc2 = (first[0] - first_next[0]) * (second_next[1] - first[1]) + (first[1] - first_next[1]) * (first[0] - second_next[0])
    td1 = (second[0] - second_next[0]) * (first[1] - second[1]) + (second[1] - second_next[1]) * (second[0] - first[0])
    td2 = (second[0] - second_next[0]) * (first_next[1] - second[1]) + (second[1] - second_next[1]) * (second[0] - first_next[0])
    return tc1 * tc2 <= 0 and td1 * td2 <= 0


# In[7]:


# when the two lines intersect each other, reorganize the points so that there is no intersections
def noCross(cities, tour, total_distance):
    continue_flag = True
    while continue_flag:
        continue_flag = False
        N = len(cities)
        for i in range (1, N-2):
            for j in range(i+2, N-1):
                if judgeCross(i, j, cities, tour):
                    #from IPython.core.debugger import Pdb; Pdb().set_trace()
                    tour, temp_distance = fixChain(cities, tour, total_distance, i, j)
                    if temp_distance<total_distance:
                        continue_flag = True
                        total_distance = temp_distance
    
    return tour, total_distance


# In[8]:


# changing the order of the tour and re-calculate the distance of the given two points
def fixChain(cities, tour, total_distance, start, end):
    new_tour = tour[:]
    new_total_distance = 0
    for i in range (end-start):
        new_tour[start+i+1]=tour[end-i]
        
    N = len(cities)
    
    for i in range (N-1):
        new_total_distance += distance(cities[new_tour[i]], cities[new_tour[i+1]])
        
    return new_tour, new_total_distance


# In[9]:


# simulated annealing
def annealing(cities, tour, total_distance, initial_distance, start_time, time_limit):
    first = random.randrange(len(tour))
    second = random.randrange(len(tour))
    
    if first==0 or second ==0:
        return tour, total_distance
    if first==len(tour)-1 or second==len(tour)-1:
        return tour, total_distance
    if first==second:
        return tour, total_distance
    
    new_tour, new_total_distance = swapRoute(cities, tour, total_distance, first, second) #TODO
    
    rand = random.random()
    probability = getProbability(start_time, time_limit, new_total_distance, total_distance, initial_distance)
    
    print(str(probability)+" , "+str(rand)+" , "+str(new_total_distance)+" , "+str(total_distance))
    
#     Annealing1
    if probability>rand:
        tour = new_tour
        total_distance = new_total_distance

#   Annealing2
#     if new_total_distance < total_distance:
#         tour = new_tour
#         total_distance = new_total_distance
    
    return tour, total_distance


# In[10]:


# creating an initial answer based on greedy technique
def greedy(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]
    total_distance = 0
    
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        total_distance += dist[current_city][next_city]
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
        
        
    total_distance += dist[current_city][tour[0]]
    tour.append(tour[0])
    return tour, total_distance


# In[11]:


# do brute-force method if the number of cities is small
def brute(cities, tour, total_distance):
    if len(cities)<9:
        now_place = 0
        visited = [False] * len(cities)
        visited[0]=True
        count_visited = 1
        now_distance = 0
        now_tour = [0]
        tour, total_distance = run_brute(cities, tour, now_tour, now_distance, now_place, visited, count_visited, total_distance)
    
    return tour, total_distance


def run_brute (cities, tour, now_tour, now_distance, now_place, visited, count_visited, min_distance):
    if count_visited == len(cities):
        now_distance += distance(cities[now_place], cities[0])
        now_tour.append(0)
        if now_distance<min_distance:
            tour = now_tour
            min_distance = now_distance
        return tour, min_distance
        
    for i in range (len(cities)):
        if visited[i]:
            continue
            
        visited[i]=True
        next_tour = now_tour[:]
        next_tour.append(i)
        next_distance = now_distance + distance(cities[now_place], cities[i])
        tour, min_distance = run_brute (cities, tour, next_tour, next_distance, i, visited, count_visited+1, min_distance)
        visited[i]=False
        
    return tour, min_distance


# In[12]:


# method for creating an initial answer and calling functions to improve it
def solve(cities):
    tour, total_distance = greedy(cities)
    start_time = time.time()
    time_limit = 1
    initial_distance = total_distance
    while (time.time()-start_time<time_limit):
        tour, total_distance = annealing(cities, tour, total_distance, initial_distance, start_time, time_limit)
    tour, total_distance = noCross(cities, tour, total_distance)
    tour, total_distance = brute(cities, tour, total_distance)
    #from IPython.core.debugger import Pdb; Pdb().set_trace()
    return tour


# In[13]:


# reading input from csv file
def readInput(count):
    with open("input_"+str(count)+".csv", encoding='utf-8') as csvfile:
        cities = []
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row
        for row in csvreader:
            x, y = float(row[0]), float(row[1])
            cities.append([x, y])
    
    return cities


# In[14]:


# writing the answer as a csv file
def writeOutput(tour, count):
    
    tour = tour[:-1]
    
    with open('output_'+str(count)+".csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header
        csvwriter.writerow(['index'])
        # Write the tour indices
        for location in tour:
            csvwriter.writerow([location])


# In[15]:


if __name__ == '__main__':
#     for i in range (7):
#         cities = readInput(i)
#         tour = solve(cities)
#         writeOutput(tour, i)
#         print("Finished "+str(i)+"th data!")

# When testing for one particular test case
    i = 5
    cities = readInput(i)
    tour = solve(cities)
    writeOutput(tour, i)
    print("Finished "+str(i)+"th data!")

