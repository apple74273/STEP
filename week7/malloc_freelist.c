#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void* mmap_from_system(size_t size);
void munmap_to_system(void* ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
    size_t size;
    struct my_metadata_t* next;
} my_metadata_t;

typedef struct my_heap_t {
    my_metadata_t* free_head;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap[200];

//
// Helper functions (feel free to add/remove/edit!)
//

// Calculate the index of the free bin
int find_index_of_the_bin(size_t size) {
    int index = size / 20;
    if (index > 199) {
        index = 199;
    }
    return index;
}

void my_add_to_free_list(my_metadata_t* metadata) {
    int index = find_index_of_the_bin(metadata->size);
    metadata->next = my_heap[index].free_head;
    my_heap[index].free_head = metadata;

}

void my_remove_from_free_list(my_metadata_t* metadata, my_metadata_t* prev) {
    int index = find_index_of_the_bin(metadata->size);
    if (prev) {
        prev->next = metadata->next;
    }
    else {
        my_heap[index].free_head = metadata->next;
    }
    metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
    for (int i = 0; i < 200; i++) {
        my_heap[i].free_head = NULL;
    }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void* my_malloc(size_t size) {
    int index = find_index_of_the_bin(size);
    my_metadata_t* metadata = my_heap[index].free_head;
    my_metadata_t* prev = NULL;

    size_t best_difference = SIZE_MAX; // Initialize to maximum value of size_t
    my_metadata_t* best_metadata = NULL;
    my_metadata_t* best_prev = NULL;

    // Find the best-fit free slot
    while (index < 200) {
        metadata = my_heap[index].free_head;
        prev = NULL; // Reset prev when moving to the next bin
        while (metadata) {
            if (metadata->size >= size) {
                size_t difference = metadata->size - size;
                if (best_difference > difference) {
                    best_difference = difference;
                    best_metadata = metadata;
                    best_prev = prev;

                    // No better option will appear if the difference is zero
                    if (best_difference == 0) {
                        break;
                    }
                }
            }

            prev = metadata;
            metadata = metadata->next;
        }
        if (best_metadata) {
            break;
        }
        else {
            index += 1;
        }
    }

    metadata = best_metadata;
    prev = best_prev;

    // If no suitable block was found, request more memory from the system
    if (!metadata) {
        size_t buffer_size = 4096;
        metadata = (my_metadata_t*)mmap_from_system(buffer_size);
        metadata->size = buffer_size - sizeof(my_metadata_t);
        metadata->next = NULL;
        // Add the new block to the free list and try allocation again
        my_add_to_free_list(metadata);
        return my_malloc(size);
    }

    void* ptr = metadata + 1;
    size_t remaining_size = metadata->size - size;
    // Remove the allocated slot from the free list
    my_remove_from_free_list(metadata, prev);

    if (remaining_size > sizeof(my_metadata_t)) {
        // Split the block if there is enough space left for a new metadata
        metadata->size = size;
        my_metadata_t* new_metadata = (my_metadata_t*)((char*)ptr + size);
        new_metadata->size = remaining_size - sizeof(my_metadata_t);
        new_metadata->next = NULL;
        // Add the remaining free slot to the free list
        my_add_to_free_list(new_metadata);
    }

    return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void* ptr) {
    my_metadata_t* metadata = (my_metadata_t*)ptr - 1;
    // Add the freed slot back to the free list
    my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
    // Nothing is here for now.
    // Feel free to add something if you want!
}

void test() {
    // Implement test cases if needed
    assert(1 == 1); // Placeholder for actual test cases
}
