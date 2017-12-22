#
# searcher.py (Final project)
#
# classes for objects that perform state-space search on Eight Puzzles  
#
# name: Rena Auerbach
# email: renaauer@bu.edu
#
# If you worked with a partner, put his or her contact info below:
# partner's name:
# partner's email:
#

import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    ### Add your Searcher method definitions here. ###
    def __init__(self, depth_limit):
        """constructor for Searcher object"""
        self.states = []
        self.num_tested = 0
        self.depth_limit = depth_limit
        
    
    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s

    def add_state(self, new_state):
        """adds a single State object (new_state) to the Searcher‘s list
        of untested states
        """
        self.states += [new_state]


    def should_add(self, state):
        """returns True if the called Searcher should add state to its list
        of untested states, and returns False otherwise
        """
        if state.num_moves > self.depth_limit and self.depth_limit != -1:
            return False
        elif state.creates_cycle() == True:
            return False
        else:
            return True

        
    def add_states(self, new_states):
        """processes the elements of new_states individually
        input: a list State object
        """
        for s in new_states:
            if self.should_add(s) == True:
                self.add_state(s)


    def next_state(self):
        """ chooses the next state to be tested from the list of 
        untested states, removing it from the list and returning it
        """
        s = random.choice(self.states)
        self.states.remove(s)
        return s


    def find_solution(self, init_state):
        """performs a full state-space search that begins at the specified
        initial state init_state and ends when the goal state is found or
        when the Searcher runs out of untested states
        """
        self.add_state(init_state)
        while len(self.states) > 0:
            self.num_tested += 1
            s = self.next_state()
            if s.is_goal() == True:
                return s
            else:
                self.add_states(s.generate_successors())
        return None
        

### Add your BFSeacher and DFSearcher class definitions below. ###
class BFSearcher(Searcher):
    """ A class that inherits from Searcher, but performs a breadth-first
        search (BFS) of an Eight Puzzle.
    """
    def next_state(self):
        """overrides the next_state method in Searcher.
        This version follows first-in first-out (FIFO) ordering, choosing
        the state that has been in the list the longest.
        """
        s = self.states[0]
        self.states.remove(s)
        return s


class DFSearcher(Searcher):
    """ A class that inherits from Searcher, but performs a depth-first
        search (DFS) of an Eight Puzzle.
    """
    def next_state(self):
        """overrides the next_state method in Searcher.
        This version follows last-in first-out (LIFO) ordering, choosing
        the state that was most recently added to the list.
        """
        s = self.states[-1]
        self.states.remove(s)
        return s


def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

### Add your other heuristic functions here. ###

def h1(state):
    """a heuristic function that computes and returns an estimate of how many
    additional moves are needed to get from state to the goal state (the
    number of misplaced tiles in the Board object associated with state)
    """
    est = state.board.num_misplaced()
    return est

def h2(state):
    """a heuristic function that computes and returns an estimate of how many
    additional moves are needed to get from state to the goal state (not just
    the number of misplaced tiles in the Board object)
    """
    total = state.board.solver()
    return total


class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """
    ### Add your GreedySearcher method definitions here. ###
    
    def __init__(self, heuristic):
        """constructor for GreedySearcher object"""
        Searcher.__init__(self, -1)
        self.heuristic = heuristic


    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s

        
    def priority(self, state):
        """ computes and returns the priority of the specified state,
            based on the heuristic function used by the searcher
        """
        return -1 * self.heuristic(state)


    def add_state(self, state):
        """overrides add_state method that is inherited from Searcher.
        This version adds a sublist [priority, state] pair, where priority
        is the priority of state that is determined by calling the priority
        method
        """
        self.states += [[self.priority(state), state]]


    def next_state(self):
        """overrides the next_state method inherited from Searcher.
        This version should choose one of the states with the highest priority
        """
        s = max(self.states)
        self.states.remove(s)
        return s[1]


### Add your AStarSeacher class definition below. ###
class AStarSearcher(GreedySearcher):
    """ A class for Searcher objects, inheritting from GreedySearcher, that
    perform A* search"""

    def priority(self, state):
        """overrides the priority method from GreedySearcher.
        This version takes into account the number of moves to get to that
        state
        """
        num_tested = len(self.states)
        return -1 * (self.heuristic(state) + num_tested)

