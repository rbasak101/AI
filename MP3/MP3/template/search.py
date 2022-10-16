# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
import heapq

# Search should return the path and the number of states explored.
# The path should be a list of MazeState objects that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (astar)
# You may need to slight change your previous search functions in MP2 since this is 3-d maze
def search(maze, searchMethod):
    return {
        "astar": astar,
    }.get(searchMethod, [])(maze)

def astar(maze, ispart1=False):
    """
    This function returns an optimal path in a list, which contains the start and objective.

    @param maze: Maze instance from maze.py
    @param ispart1:pass this variable when you use functions such as getNeighbors and isObjective. DO NOT MODIFY THIS
    @return: a path in the form of a list of MazeState objects. If there is no path, return None.
    """
    # Your code here
    print("astar, maze printing")
    print(len(maze.get_map()), len(maze.get_map()[1]))
    print("Dimensions: ", maze.getDimensions())  # row, col, level
    dim = maze.getDimensions()
    # outputMap = ""
    # for l in range(dim[2]):
    #     for i in range(dim[0]):
    #         for j in range(dim[1]):
    #             outputMap += maze.get_map()[i][j][l]
    #         outputMap += "\n"
    #     outputMap += "#\n"
    # print(outputMap)

    
    # maze.saveToFile("figuring_out_part3")
    # print("Saveed to file?")
    path = []
    # return None
    # starting_tuple = maze.getStart()  # (row, col, level)
    # starting_state = MazeState(starting_tuple, maze.getObjectives(), 0, maze, mst_cache={}, use_heuristic=True)
    starting_state = maze.getStart()
    print("Astar starting point: ", starting_state, type(starting_state))
    visited_states = {starting_state: (None, 0)}
    

    min_heap = []
    heapq.heappush(min_heap, starting_state)
    while min_heap:
        abstract_state = heapq.heappop(min_heap)
        print(" SEARCH current: ", abstract_state)
        # print("SEARCH is goal: ", abstract_state.is_goal())
        if abstract_state.is_goal():
            print("Found closest goal")
            path = backtrack(visited_states, abstract_state)
            return path


        neighbors = abstract_state.get_neighbors(ispart1)
        for n in neighbors:
            if n not in visited_states:
                distance = (n.dist_from_start + n.h)
                visited_states[n] = (abstract_state, distance)
                heapq.heappush(min_heap, n)
            elif visited_states[n][1] > (n.dist_from_start + n.h):
                visited_states[n] = (abstract_state, distance)
                heapq.heappush(min_heap, n)
        
        # print("minheap: ", min_heap)
        print(" ")
    return None

        # if abstract_state.is_goal():
        #     # print("found goal!", abstract_state)
        #     path = backtrack(visited_states, abstract_state)
        #     return path

        # neighbors = abstract_state.get_neighbors()
        # print("Neighbors: ", neighbors)
        # for n in neighbors:
        #     # distance = (n.dist_from_start + n.h) * 1
        #     if n not in visited_states:
                    
                
        #         # print(type(n), n)
        #         distance = (n.dist_from_start + n.h) 
        #         # print("pushing: ", n, " ", distance)
        #         visited_states[n] = (abstract_state, distance)

        #         heapq.heappush(min_heap, n)
        #     elif visited_states[n][1] > (n.dist_from_start + n.h) :
        #         visited_states[n] = (abstract_state, distance)
        #         heapq.heappush(min_heap, n)
        #     print(" ")
        #     print(" ")
        # print("min heap: ", min_heap)
        # print(" ")
        # print(visited_states)
        # print("-------------------------")

    # return None

# This is the same as backtrack from MP2
def backtrack(visited_states, current_state):
    path = []
    while int(current_state.dist_from_start) != 0:
        path.append(current_state)
        current_state = visited_states[current_state][0]

    path.append(current_state)
    path = path[::-1]
    print("path: ", path)
    return path
        