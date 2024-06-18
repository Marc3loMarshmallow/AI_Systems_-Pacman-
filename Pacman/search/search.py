# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    from util import Stack

    expl = []
    stack = Stack()
    stack.push((problem.getStartState(),[]))

    while not stack.isEmpty():
        curNodeObj = stack.pop()
        curNode = curNodeObj[0]
        expl.append(curNode)
        
        if problem.isGoalState(curNode):
            return curNodeObj[1]
        for successor in problem.getSuccessors(curNode):
            if successor[0] not in expl:
                
                newDirections = list(curNodeObj[1])
                newDirections.append(successor[1])
                stack.push((successor[0], newDirections))
    return -1

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    
    expl = []
    queue = Queue()
    queue.push((problem.getStartState(),[]))
   
    while not queue.isEmpty():
        curNodeObj = queue.pop()
        curNode = curNodeObj[0]

        if problem.isGoalState(curNode) == True:
            return curNodeObj[1]
            
        if curNode not in expl:
            expl.append(curNode)
            #print('succ\n')
            for successor in problem.getSuccessors(curNode):
                if successor[0] not in expl:
                    #print( successor)
                    newDirections = list(curNodeObj[1])
                    newDirections.append(successor[1])
                    queue.push((successor[0], newDirections))
    return -1

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    
    queue = PriorityQueue()
    queue.push(([problem.getStartState()],[]), 0)
    bestResult = 10000000000000000000000000000000000000000000000000 # hopefully it is large enough to overcome threshold
    bestPath = -1 # If there is no terminal state or for some reason it can not be reached, then -1 will be returned.
    expl = []
    
    while not queue.isEmpty():
        curNodeObj = queue.pop()
        curNode = curNodeObj[0][-1]

        # Check a goal node and update the current best result and path.
        if problem.isGoalState(curNode):
            if problem.getCostOfActions(curNodeObj[1]) < bestResult:
                bestResult = problem.getCostOfActions(curNodeObj[1])
                bestPath = curNodeObj[1]
            continue # there is no need to expand a terminal node

        # First check if a node was already expanded
        if curNode not in expl:
        
            # If not then compare the current path with the best result.
            # If it is better then we can expand the node. If it is worse then we have to let it be, maybe it will produce better results later.
            if problem.getCostOfActions(curNodeObj[1]) < bestResult:
                expl.append(curNode) 
                
                for successor in problem.getSuccessors(curNode):
                    if successor[0] not in expl:
                        newPath = list(curNodeObj[0])
                        newPath.append(successor[0])
                        newDirections = list(curNodeObj[1])
                        newDirections.append(successor[1])
                        queue.update((newPath, newDirections),problem.getCostOfActions(newDirections))             
    return bestPath


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
    
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue
    
    expl = []
    Queue = PriorityQueue()
    Queue.push(([problem.getStartState()],[],0),0)
    
    while not Queue.isEmpty():
        curNodeObj = Queue.pop()
        curNode = curNodeObj[0][-1]        
        
        if problem.isGoalState(curNode):
            return curNodeObj[1]

        if curNode not in expl:
            expl.append(curNode) 
            for successor in problem.getSuccessors(curNode):
                if successor[0] not in expl:
                    newPath = list(curNodeObj[0])
                    newPath.append(successor[0])
                    newDirections = list(curNodeObj[1])
                    newDirections.append(successor[1])
                    Queue.update((newPath, newDirections), problem.getCostOfActions(newDirections)+heuristic(successor[0], problem))
    return -1

#Practically just like the A* but without the getCostOfActions.
def GreedyBestFirstSearch(problem, heuristic):
    from util import PriorityQueue
    print(problem.goal)
    expl = []
    Queue = PriorityQueue()
    Queue.push(([problem.getStartState()],[],0),0)
    
    while not Queue.isEmpty():
        curNodeObj = Queue.pop()
        curNode = curNodeObj[0][-1]       
        
        if problem.isGoalState(curNode):
            return curNodeObj[1]

        if curNode not in expl:
            expl.append(curNode) 
            for successor in problem.getSuccessors(curNode):
                if successor[0] not in expl:
                    newPath = list(curNodeObj[0])
                    newPath.append(successor[0])
                    newDirections = list(curNodeObj[1])
                    newDirections.append(successor[1])
                    Queue.update((newPath, newDirections), heuristic(successor[0], problem))
    return -1

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
