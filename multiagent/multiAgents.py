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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList() 
        ghostPositions = []

        # For each ghost in the newGhostStates, get its position and append it to the ghostPositions list
        for ghost in newGhostStates:
            ghostPosition = ghost.getPosition()[0], ghost.getPosition()[1]
            ghostPositions.append(ghostPosition)

        # Check if the ghost is scared by seeing if the first element in newScaredTimes is greater than 0
        isScared = newScaredTimes[0] > 0

        # If the ghost is not scared and the new position is in the ghost positions, return -1
        if isScared == False and (newPos in ghostPositions):
            return -1
        # If the new position is in the list of food positions in the current game state, return 1
        if newPos in currentGameState.getFood().asList():
            return 1

        # Sort the food list and ghost positions list based on their manhattan distance from the new position
        nearestFoodDist = sorted(foodList, key=lambda foodDistance: util.manhattanDistance(foodDistance, newPos))
        nearestGhostDist = sorted(ghostPositions, key=lambda ghostDistance: util.manhattanDistance(ghostDistance, newPos))
        
        foodDistance = lambda foodDist: util.manhattanDistance(foodDist, newPos)
        ghostDistance = lambda ghostDist: util.manhattanDistance(ghostDist, newPos)

        # Return the reciprocal of the manhattan distance to the nearest food minus the reciprocal of the manhattan distance to the nearest ghost
        return 1 / foodDistance(nearestFoodDist[0]) - 1/ghostDistance(nearestGhostDist[0])


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
        "*** YOUR CODE HERE ***"

        bestValue = -9999999.0
        bestAction = Directions.STOP

        # Iterate over all legal actions for the current game state
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            newValue = self.getValue(nextState, 0, 1)

            # If the new value is better than the best value, update the best value and the best action
            if newValue > bestValue:
                bestValue = newValue
                bestAction = action
        return bestAction


    def getValue(self, gameState, currentDepth, agentIndex):
        # If the current depth equals the maximum depth or the game is won or lost, return the evaluation function value
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Initialize the value to a very small number if the agent is Pacman (agentIndex 0), or to a very large number otherwise
        bestValue = -9999999.0 if agentIndex == 0 else 9999999.0
        
        # Iterate over all legal actions for the current agent
        for action in gameState.getLegalActions(agentIndex):
            # If the agent is Pacman, update the value with the maximum of the current value and the value of the next state
            if agentIndex == 0:
                bestValue = max(bestValue, self.getValue(gameState.generateSuccessor(0, action), currentDepth, 1))
           
            # If the agent is the last ghost, update the value with the minimum of the current value and the value of the next state, and increase the depth
            elif agentIndex == gameState.getNumAgents()-1:
                bestValue = min(bestValue, self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth + 1, 0))
           
            # If the agent is a ghost but not the last one, update the value with the minimum of the current value and the value of the next state
            else:
                bestValue = min(bestValue, self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1))
        return bestValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        # Initialize alpha and beta values
        alpha= -9999999.0
        beta= 9999999.0

        # Initialize the best value and action
        bestValue = -9999999.0
        bestAction = Directions.STOP
        
        # Iterate over all possible actions and update the best value and action and retun the best action
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            bestValue = max(bestValue, self.getValue(nextState,0 ,1 ,alpha,beta ))

            # If the value of the current action is better than the best known value, update alpha and the best action.
            if bestValue > alpha:
                alpha = bestValue
                bestAction = action

        return bestAction


    def getValue(self, gameState, currentDepth, agentIndex, alpha, beta):


        # If the game is over or the maximum depth is reached, return the evaluation function value
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # If the agent is the maximizing agent (agentIndex == 0), find the maximum value over all actions
        if agentIndex == 0:
            bestValue = -9999999.0
            index = 1
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                bestValue = max(bestValue, self.getValue(successor ,currentDepth ,index ,alpha ,beta ))
                if bestValue > beta:
                    return bestValue
                alpha = max(alpha, bestValue)
            return bestValue

        # If the agent is a minimizing agent, find the minimum value over all actions
        else:
            bestValue= 9999999.0
            if agentIndex == gameState.getNumAgents()-1:
                currentDepth = currentDepth + 1
                index = 0
            else:
                index= agentIndex + 1
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                bestValue=min(bestValue,self.getValue(successor, currentDepth ,index ,alpha ,beta ))
                if bestValue<alpha:
                    return bestValue
                beta=min(bestValue,beta)
            return bestValue


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
