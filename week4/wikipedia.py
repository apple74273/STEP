#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import collections
from collections import deque


# In[2]:


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file, encoding='utf-8') as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file, encoding='utf-8') as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()
    
    def count_shortest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=False)
        print("Examples of shortest titles are:")
        count = 0
        index = 0
        while index < len(titles):
            if titles[index].find("_") == -1:
                if len(titles[index])!=1:
                    break
                count += 1
                if count<=10:
                    print(titles[index])
            index += 1
        print("There are "+ str(count)+" titles having the same length")


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    def find_id_from_title (self, target):
        for id in self.titles.keys():
            if self.titles[id]==target:
                return id
        
        return -1

    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = self.find_id_from_title(start)
        goal_id = self.find_id_from_title(goal)
        queue = deque()
        visited = set()
        visited.add(start_id)
        queue.append(start_id)
        prev = {}
            
        prev[start_id]=-1
        while not queue.count==0:
            node = queue.popleft()
            if node == goal_id:
                self.print_route(prev, goal_id)
                return
            for child in self.links[node]:
                if not child in visited:
                    prev[child]=node
                    visited.add(child)
                    queue.append(child)
        
        print ("No path was found")

    # trace back the routes and print out them
    def print_route(self, prev, goal_id):
        current = goal_id
        answer = []
        while(not current==-1):
            answer.append(self.titles[current])
            current = prev[current]
        
        answer.reverse()
        print (answer)
        print ("The total path length was: "+str(len(answer)))
    
    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        page_rank = {}
        for id in self.titles.keys():
            page_rank[id]=1.0
        
        count = 0
        while (True):
            count+=1
            print(count)
            new_page_rank = {}
            sum = 0
            for id in self.titles.keys():
                new_page_rank[id]=0

            for id in self.titles.keys():
                prev_rank = page_rank[id]
                if len(self.links[id])==0:
                    sum += prev_rank
                else:
                    give_rank = prev_rank * 0.85 / len(self.links[id])
                    
                    for child in self.links[id]:
                        new_page_rank[child]+=give_rank
                        
                    sum += prev_rank * 0.15
            
            for id in self.titles.keys():
                new_page_rank[id] += sum/len(self.titles)
            
            
            total_dif = 0
            
            for id in self.titles.keys():
                dif = page_rank[id]-new_page_rank[id]
                total_dif += dif*dif
            
            if total_dif<0.01:
                break
            else:
                page_rank = new_page_rank
                
        
        highest_rank = -1
        highest_id = -1
        
        for id in self.titles.keys():
            if highest_rank<page_rank[id]:
                highest_rank = page_rank[id]
                highest_id = id
        
        print("The most popular page is: "+self.titles[highest_id])


    # Do something more interesting!!
    def find_something_more_interesting(self):
        self.count_shortest_titles()
        pass


# In[3]:


if __name__ == "__main__":
    pages_file = "pages_medium.txt"
    links_file = "links_medium.txt"

    wikipedia = Wikipedia(pages_file, links_file)
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()
    wikipedia.find_something_more_interesting()

