# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the bestIndices

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** CS5368 YOUR CODE HERE ***"
        "Decribe your function:"

        # need to Check for the closest food near to the pacman and compute the distance between the position of the pacman to the food by using manhattandistance
        # next need to find the closest ghosts postions to the pacman
        # then we compute the score according to the nearest food and the ghost positions

        if action == 'Stop':
            return -100000
        # get closest food for the pacman to eat
        cFood = None
        cFoodDist = float('inf')
        for k in newFood.asList():
            fDist = manhattanDistance(k, newPos)
            if fDist < cFoodDist:
                cFood = k
                cFoodDist = fDist

        j = 0
        if cFood:
            mDist = manhattanDistance(newPos, cFood)
            j -= mDist * .25

        # information about the ghost positions
        ghostPos = []
        for ghostState in newGhostStates:
            g = ghostState.configuration.pos
            ghostPos.append(g)

        cGhost = None
        cGhostDist = float('inf')
        for g in ghostPos:
            dist = manhattanDistance(newPos, g)
            if dist < cGhostDist:
                cGhostDist = dist
                cGhost = g
        if cGhostDist <= 3:
            j -= (3 - cGhostDist) * 1000

        j += successorGameState.data.score

        if newPos == currentGameState.getPacmanPosition():
            j -= 1
        return j

        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def max_function(self, gameState, numofGhosts, plyCount):
        if gameState.isWin() or gameState.isLose() or plyCount == 0:
            return self.evaluationFunction(gameState)

        eval = []
        legalAct = gameState.getLegalActions()

        for action in legalAct:
            eval.append(self.min_function(gameState.generateSuccessor(self.index, action), numofGhosts, plyCount))

        return max(eval)

    def min_function(self, gameState, numofGhosts, plyCount):
        if gameState.isWin() or gameState.isLose() or plyCount == 0:
            return self.evaluationFunction(gameState)

        eval = []

        tNumGhosts = gameState.getNumAgents() - 1
        cGhostIndex = tNumGhosts - numofGhosts + 1
        legalAct = gameState.getLegalActions(cGhostIndex)
        if numofGhosts > 1:
            for action in legalAct:
                eval.append(self.min_function(gameState.generateSuccessor(cGhostIndex, action), numofGhosts - 1, plyCount))
        else:
            for action in legalAct:
                eval.append(self.max_function(gameState.generateSuccessor(cGhostIndex, action), tNumGhosts, plyCount - 1))

        return min(eval)


    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** CS5368 YOUR CODE HERE ***"
        "PS. It is okay to define your own new functions. For example, value, min_function,max_function"
        actions = []
        eval = []

        # import pdb; pdb.set_trace()
        for action in gameState.getLegalActions():
            actions.append(action)
            numofGhosts = gameState.getNumAgents() - 1
            eval.append(self.min_function(gameState.generateSuccessor(self.index, action), numofGhosts, self.depth))

        print("\n")
        print(gameState)
        maxEvaIndex = eval.index(max(eval))
        return actions[maxEvaIndex]

        # need to return an action not a value
        # return self.max_function(gameState, self.depth, gameState.getNumAgents() - 1)
        # use recursive helper function to make the best choice
        # every time everyone has taken an action, it's depth 1
        # return one of the legal actions

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def max_function(self, gameState, numofGhosts, plyCount, alpha, beta):
        if gameState.isWin() or gameState.isLose() or plyCount == 0:
            return self.evaluationFunction(gameState)

        legalAct = gameState.getLegalActions()
        n = - float('inf')
        for action in legalAct:
            successorState = gameState.generateSuccessor(self.index, action)
            n = max(n, self.min_function(successorState, numofGhosts, plyCount, alpha, beta))
            if n > beta:
                return n
            alpha = max(alpha, n)
        return n

    def min_function(self, gameState, numofGhosts, plyCount, alpha, beta):
        if gameState.isWin() or gameState.isLose() or plyCount == 0:
            return self.evaluationFunction(gameState)

        tNumGhosts = gameState.getNumAgents() - 1
        cGhostIndex = tNumGhosts - numofGhosts + 1
        legalAct = gameState.getLegalActions(cGhostIndex)
        n = float('inf')
        if numofGhosts > 1:
            for action in legalAct:
                successorState = gameState.generateSuccessor(cGhostIndex, action)
                n = min(n, self.min_function(successorState, numofGhosts - 1, plyCount, alpha, beta))
                if n < alpha:
                    return n
                beta = min(beta, n)
        else:
            for action in legalAct:
                successorState = gameState.generateSuccessor(cGhostIndex, action)
                n = min(n, self.max_function(successorState, tNumGhosts, plyCount - 1, alpha, beta))
                if n < alpha:
                    return n
                beta = min(beta, n)
        return n



    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** CS5368 YOUR CODE HERE ***"
        "PS. It is okay to define your own new functions. For example, value, min_function,max_function"
        actions = []
        eval = []

        alpha = - float('inf')
        beta = float('inf')
        n = - float('inf')
        for action in gameState.getLegalActions():
            actions.append(action)
            numofGhosts = gameState.getNumAgents() - 1
            successorState = gameState.generateSuccessor(self.index, action)
            n = max(n, self.min_function(successorState, numofGhosts, self.depth, alpha, beta))
            if n > beta:
                return n
            alpha = max(alpha, n)

            eval.append(n)

        maxEvaIndex = eval.index(max(eval))
        return actions[maxEvaIndex]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def max_function(self, gameState, numofGhosts, plyCount):
        if gameState.isWin() or gameState.isLose() or plyCount == 0:
            return self.evaluationFunction(gameState)

        eval = []
        legalAct = gameState.getLegalActions()

        for action in legalAct:
            eval.append(self.min_function(gameState.generateSuccessor(self.index, action), numofGhosts, plyCount))

        return max(eval)

    def min_function(self, gameState, numofGhosts, plyCount):
        if gameState.isWin() or gameState.isLose() or plyCount == 0:
            return self.evaluationFunction(gameState)

        tNumGhosts = gameState.getNumAgents() - 1
        cGhostIndex = tNumGhosts - numofGhosts + 1
        legalAct = gameState.getLegalActions(cGhostIndex)
        sum = 0.0
        if numofGhosts > 1:
            for action in legalAct:
                sum += float(
                    self.min_function(gameState.generateSuccessor(cGhostIndex, action), numofGhosts - 1, plyCount))
        else:
            for action in legalAct:
                sum += float(
                    self.max_function(gameState.generateSuccessor(cGhostIndex, action), tNumGhosts, plyCount - 1))
        # print("min eval:")
        # print(eva)
        return sum / (len(legalAct))

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** CS5368 YOUR CODE HERE ***"
        "PS. It is okay to define your own new functions. For example, value, min_function,max_function"
        actions = []
        eval = []

        for action in gameState.getLegalActions():
            actions.append(action)
            numofGhosts = gameState.getNumAgents() - 1
            eval.append(self.min_function(gameState.generateSuccessor(self.index, action), numofGhosts, self.depth))

        maxEvaIndex = eval.index(max(eval))
        return actions[maxEvaIndex]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    #Check for the closest food near to the pacman and compute the distance between the position of the pacman to the food using manhattandistance
    #Find the ghosts postions in the state space
    #Compute the manhattan distance between the ghost and the pacman:
             #Now if the manhattan distance is less than 10 -> chase after the ghost
                 #If the ghost is scared -> go towards the closest food
             #If the manhattan distance is less than or equal to 3 -> run away from the ghost
    "*** CS5368 YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # get closest food for the pacman to eat
    cFood = None
    cFoodDist = float('inf')
    for k in newFood.asList():
        fDist = manhattanDistance(k, newPos)
        if fDist < cFoodDist:
            cFood = k
            cFoodDist = fDist

    j = 0
    if cFood:
        mDist = manhattanDistance(newPos, cFood)
        j -= mDist * .25

    # information about the ghost positions
    ghostPos = []
    for ghostState in newGhostStates:
        g = ghostState.configuration.pos
        ghostPos.append(g)

    scaredGhostIndex = newScaredTimes.index(max(newScaredTimes))
    ghostScared = newScaredTimes[scaredGhostIndex]
    cGhostDist = float('inf')
    for g in ghostPos:
        dist = manhattanDistance(newPos, g)
        if dist < cGhostDist:
            cGhostDist = dist
    if not ghostScared and cGhostDist <= 3:
        j -= (3 - cGhostDist) * 1000
    else:
        for time in newScaredTimes:
            scaredGhostPos = newGhostStates[newScaredTimes.index(time)].configuration.pos
            distToScaredGhost = manhattanDistance(newPos, scaredGhostPos)
            if time > 0 and distToScaredGhost < 10:
                j += distToScaredGhost

    j += currentGameState.data.score

    if newPos == currentGameState.getPacmanPosition():
        j -= 1

    return j

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
