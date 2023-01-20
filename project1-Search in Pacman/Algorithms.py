import util

class DFS(object):
    def depthFirstSearch(self, problem):
        """
        Search the deepest nodes in the search tree first
        [2nd Edition: p 75, 3rd Edition: p 87]

        Your search algorithm needs to return a list of actions that reaches
        the goal.  Make sure to implement a graph search algorithm
        [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

        To get started, you might want to try some of these simple commands to
        understand the search problem that is being passed in:

        print "Start:", problem.getStartState()
        print "Is the start a goal?", problem.isGoalState(problem.getStartState())
        print "Start's successors:", problem.getSuccessors(problem.getStartState())
        """
        "*** TTU CS5368 YOUR CODE HERE ***"

        fringe = util.Stack()
        startState = problem.getStartState()
        #pushing start state and the empty list to the fringe
        fringe.push((startState, []))
        visited = []
#if fringe is not empty we are removing the tuple which consists of currnode and it's respective currvalue. this loop executes
       # until fringe becomes empty
        while not fringe.isEmpty():
            curNode, curValue = fringe.pop()
#if the current node and the goal state are same then it returns the current value
            if problem.isGoalState(curNode):
                return curValue
#if the currentnode is not in the visted list then we are adding the current node to visted list
            if curNode not in visited:
                visited.append(curNode)
#gets all the Successors of current node and stores in variable nxtchild
                nxtChild = problem.getSuccessors(curNode)
                # we are iterating each child in nextchild and assigning thier values to s,v,sc respectively and finally pushing them to fringe
                for child in nxtChild:
                    s, v, sc = child
                    fringe.push((s, curValue + [v]))

        return []
        util.raiseNotDefined()



class BFS(object):
    def breadthFirstSearch(self, problem):
        "*** TTU CS5368 YOUR CODE HERE ***"
        fringe = util.Queue()
        startState = problem.getStartState()
        fringe.push((startState, []))
        visited = []

        while not fringe.isEmpty():
            curNode, curValue = fringe.pop()

            if problem.isGoalState(curNode):
                return curValue

            if curNode not in visited:
                visited.append(curNode)

                nxtChild = problem.getSuccessors(curNode)
                for child in nxtChild:
                    s, v, sc = child
                    fringe.push((s, curValue + [v]))

        return []
        
        util.raiseNotDefined()

class UCS(object):
    def uniformCostSearch(self, problem):
        "*** TTU CS5368 YOUR CODE HERE ***"
        fringe = util.PriorityQueue()
        startState = problem.getStartState()
        fringe.push((startState, []), 0)
        visited = []

        while not fringe.isEmpty():
            curNode, curValue = fringe.pop()

            if problem.isGoalState(curNode):
                return curValue

            if curNode not in visited:
                visited.append(curNode)

                nxtChild = problem.getSuccessors(curNode)
                for child in nxtChild:
                    s, v, sc = child
                    # here along with s and v we are passing sc as well by adding it to the total cost needed to perform the actions of currValue

                    fringe.push((s, curValue + [v]), problem.getCostOfActions(curValue) + sc)

        return []
        util.raiseNotDefined()
        
class aSearch (object):
    def nullHeuristic( state, problem=None):
        """
        A heuristic function estimates the cost from the current state to the nearest goal in the provided SearchProblem.  This heuristic is trivial.
        """
        return 0
    def aStarSearch(self,problem, heuristic=nullHeuristic):
        "Search the node that has the lowest combined cost and heuristic first."
        "*** TTU CS5368 YOUR CODE HERE ***"
        fringe = util.PriorityQueue()
        startState = problem.getStartState()
        fringe.push((startState, []), 0)
        visited = []

        while not fringe.isEmpty():
            curNode, curValue = fringe.pop()

            if problem.isGoalState(curNode):
                return curValue
            if curNode not in visited:
                visited.append(curNode)

                nxtChild = problem.getSuccessors(curNode)
                for child in nxtChild:
                    s, v, sc = child
                    fringe.push((s, curValue + [v]), problem.getCostOfActions(curValue) + sc + heuristic(s, problem))

        return []
        util.raiseNotDefined()

