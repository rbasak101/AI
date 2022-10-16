import heapq
# You do not need any other imports

def best_first_search(starting_state):
    '''
    Implementation of best first search algorithm

    Input:
        starting_state: an AbstractState object

    Return:
        A path consisting of a list of AbstractState states
        The first state should be starting_state
        The last state should have state.is_goal() == True
    '''
    # we will use this visited_states dictionary to serve multiple purposes
    # - visited_states[state] = (parent_state, distance_of_state_from_start)
    #   - keep track of which states have been visited by the search 
    #   - keep track of the parent of each state, so we can call backtrack(visited_states, goal_state)
    #   - keep track of the distance of each state from start
    #       - if we find a shorter path to the same state we can update with the new state 
    # NOTE: we can hash states because the __hash__/__eq__ method of AbstractState is implemented
    visited_states = {starting_state: (None, 0)}

    # The frontier is a priority queue
    # You can pop from the queue using "heapq.heappop(frontier)"
    # You can push onto the queue using "heapq.heappush(frontier, state)"
    # NOTE: states are ordered because the __lt__ method of AbstractState is implemented
    min_heap = []
    heapq.heappush(min_heap, starting_state)
    
    # TODO(III): implement the rest of the best first search algorithm
    # HINTS:
    #   - add new states to the frontier by calling state.get_neighbors()
    #   - check whether you've finished the search by calling state.is_goal()
    #       - then call backtrack(visited_states, state)...
    # Your code here ---------------

    # ------------------------------
    
    # if you do not find the goal return an empty list

    """
    Pseudo:
        check if this is goal
        Get neigbors
        calculate cost or distance, mark visited then add to heap

    """
    # print(visited_states, min_heap)
    # print("BFS start")
    print("starting state: ", starting_state.state)
    while min_heap:
        abstract_state = heapq.heappop(min_heap)
        # print(" SEARCH current: ", abstract_state)
        # print("SEARCH is goal: ", abstract_state.is_goal())
        if abstract_state.is_goal():
            # print("found goal!", abstract_state)
            path = backtrack(visited_states, abstract_state)
            return path

        neighbors = abstract_state.get_neighbors()
        # print("Neighbors: ", neighbors)
        for n in neighbors:
            # distance = (n.dist_from_start + n.h) * 1
            if n not in visited_states:
                    
                
                # print(type(n), n)
                distance = (n.dist_from_start + n.h) 
                # print("pushing: ", n, " ", distance)
                visited_states[n] = (abstract_state, distance)

                heapq.heappush(min_heap, n)
            elif visited_states[n][1] > (n.dist_from_start + n.h) :
                visited_states[n] = (abstract_state, distance)
                heapq.heappush(min_heap, n)
            print(" ")
            print(" ")
        # print("min heap: ", min_heap)
        # print(" ")
        # print(visited_states)
        # print("-------------------------")


    return []




# TODO(III): implement backtrack method, to be called by best_first_search upon reaching goal_state
# Go backwards through the pointers in visited_states until you reach the starting state
# NOTE: the parent of the starting state is None
def backtrack(visited_states, goal_state):
    path = []
    current_state = goal_state
    # print("SEARCH 97: ", goal_state, " |||| ", visited_states[current_state])
    # while(visited_states[current_state][1] != 0):
    #     path.append(current_state)
    #     current_state = visited_states[current_state][0]

    while int(current_state.dist_from_start) != 0:
        path.append(current_state)
        current_state = visited_states[current_state][0]

    path.append(current_state)
    path = path[::-1]
    # print("path: ", path)
    return path