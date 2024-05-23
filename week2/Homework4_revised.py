#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys


# In[2]:


# Hash function.
#
# |key|: string
# Return value: a hash value
def calculate_hash(key):
    assert type(key) == str
    # Note: This is not a good hash function. Do you see why?
    hash = 0
    count = 1
    for i in key:
        hash += ord(i)*count
        count *= 2
    return hash


# In[3]:


# An item object that represents one key - value pair in the hash table.
class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


# In[4]:


# entry to be managed by the doublely linked list
class Entry:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    # |previous|: The previous item in the linked list. If this is the first item in the
    #         linked list, |previous| is None.
    def __init__(self, key, value, next, previous):
        self.key = key
        self.value = value
        self.next = next
        self.previous = previous


# In[5]:


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size.
# |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is |hash|.
# |self.item_count|: The total number of items in the hash table.
class HashTable:

    # Initialize the hash table.
    def __init__(self):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.
    def put(self, key, value):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        # find the place to put the input data
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            # if the hash table already has an item with the same key, it will return False
            if item.key == key:
                item.value = value
                return False
            item = item.next
        # adding the new item at the front of the list
        new_item = Item(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        
        # Checking the size of the hash table; if it becomes too small, it will rehash the content to a larger hash table
        if (self.item_count >= self.bucket_size * 0.7):
            new_bucket_size = self.bucket_size*2+1
            self.rehash(new_bucket_size)
        return True

    # Get an item from the hash table.
    #
    # |key|: The key.
    # Return value: If the item is found, (the value of the item, True) is
    #               returned. Otherwise, (None, False) is returned.
    def get(self, key):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        # calculating the place containing the key
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        
        # going down the list until it finds the item with the target key
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
            
        # coming here indicates that the target key was not found; it will return False
        return (None, False)
    
    # Rehash the table to a new size
    # new_bucket_size: new size of the table
    # Return value: void
    def rehash(self, new_bucket_size):
        # creating an array with new bucket size
        new_buckets = [None] * new_bucket_size
        
        # calculating new hash values to each entry and adding to the new hash table
        for i in range (self.bucket_size):
            item = self.buckets[i]
            
            while item!=None:
                new_bucket_index = calculate_hash(item.key) % new_bucket_size
                new_item = Item(item.key, item.value, new_buckets[new_bucket_index])
                new_buckets[new_bucket_index] = new_item
                item = item.next
        
        # updating hash table and its size
        self.buckets = new_buckets
        self.bucket_size = new_bucket_size
    
    # Delete an item from the hash table.
    #
    # |key|: The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        if key == None:
            return delete_successfully
        
        assert type(key) == str
        delete_successfully = False
        
        # calculating the place containing the target key
        bucket_index = calculate_hash(key) % self.bucket_size
        
        # going down the list until it finds an entry with the target key
        prev_item = None
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                if prev_item == None:
                    self.buckets[bucket_index] = item.next
                else:
                    prev_item.next = item.next
                delete_successfully = True
                self.item_count -= 1
                break
            prev_item = item
            item = item.next
        
        # Checking the size of the hash table; if it becomes too large, it will rehash the content to a smaller hash table
        if (self.item_count <= self.bucket_size * 0.3 and self.item_count >= 100):
            new_bucket_size = int(self.bucket_size/2)
            if new_bucket_size%2 == 0:
                new_bucket_size += 1
            self.rehash(new_bucket_size)
        
        return delete_successfully

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count

    # Check that the hash table has a "reasonable" bucket size.
    # The bucket size is judged "reasonable" if it is smaller than 100 or
    # the buckets are 30% or more used.
    #
    # Note: Don't change this function.
    def check_size(self):
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)


# In[6]:


# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!

class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    # oldest_item & newest_item = item to manage doublely linked list
    def __init__(self, n):
        self.hash_table = HashTable()
        self.oldest_entry = Entry (None, None, None, None)
        self.newest_entry = Entry (None, None, self.oldest_entry, None)
        self.oldest_entry.previous = self.newest_entry
        self.cache_count = 0
        self.cache_size = n

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        # get the entry from the hash table
        (entry, result) = self.hash_table.get(url)
        # The variable result shows whether it can find the entry with the target key (True = found)
        if result:
            # update the order of access_list
            target_entry = entry
            previous_entry = target_entry.previous
            next_entry = target_entry.next
            previous_entry.next = next_entry
            next_entry.previous = previous_entry
            
            current_new_entry = self.newest_entry.next
            self.newest_entry.next = target_entry
            target_entry.next =  current_new_entry
            target_entry.previous = self.newest_entry
            current_new_entry.previous = target_entry
        else:
            # delete the least recently accessed page and add the new page accessed right now
            if (self.cache_count==self.cache_size):
                delete_entry = self.oldest_entry.previous
                self.hash_table.delete(delete_entry.key)
                previous_entry = delete_entry.previous
                previous_entry.next = self.oldest_entry
                self.oldest_entry.previous = previous_entry
            else:
                self.cache_count+=1
                
            current_new_entry = self.newest_entry.next
            new_entry = Entry (url, contents, current_new_entry, self.newest_entry)
            current_new_entry.previous = new_entry
            self.newest_entry.next = new_entry
            self.hash_table.put(url,new_entry)

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        ans_list = []
        
        #Get the list of pages
        entry = self.newest_entry.next
        
        while entry:
            ans_list.append(entry.key)
            entry = entry.next
        
        #最後はoldest_entryになっているはずなので消す
        ans_list.pop(-1)
        
        return ans_list 


# In[7]:


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


# In[8]:


if __name__ == "__main__":
    cache_test()


# In[ ]:




