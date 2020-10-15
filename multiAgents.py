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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        score = successorGameState.getScore()

        foodList = newFood.asList()
        foodDistances = [ manhattanDistance(newPos, food) for food in foodList ]
        if len(foodDistances) > 0:
          score -= min(foodDistances)  

        ghostDistances = [ manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates ]
        score += min(ghostDistances)

        return score

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
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState, 0)[0]
        util.raiseNotDefined()

    def minimax(self, gameState, depth):
        if depth is self.depth * gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        
        agentIndex = depth % gameState.getNumAgents()
        
        if agentIndex == 0:
            return self.maxValue(gameState, depth)[1]
        
        return self.minValue(gameState, depth, agentIndex)

    def maxValue(self, gameState, depth):
        # Agent index always 0
        agentIndex = 0
        bestAction = ('', -float('inf'))
        legalActions = gameState.getLegalActions(agentIndex)
        
        for action in legalActions:
            nextGameState = gameState.generateSuccessor(agentIndex, action)
            score = self.minimax(nextGameState, depth + 1)
            if (score > bestAction[1]):
                bestAction = (action, score)
        
        return bestAction

    def minValue(self, gameState, depth, agentIndex):
        minScore = float('inf')
        legalActions = gameState.getLegalActions(agentIndex)

        for action in legalActions:
            nextGameState = gameState.generateSuccessor(agentIndex, action)
            score = self.minimax(nextGameState, depth + 1)
            minScore = min(minScore, score)

        return minScore

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState, 0, -float('inf'), float('inf'))[0]
        util.raiseNotDefined()

    def alphabeta(self, gameState, depth, alpha, beta):
        if depth is self.depth * gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        
        agentIndex = depth % gameState.getNumAgents()
        
        if agentIndex == 0:
            return self.maxValue(gameState, depth, alpha, beta)[1]
            
        return self.minValue(gameState, depth, agentIndex, alpha, beta)

    # Return (action, maxValue)
    def maxValue(self, gameState, depth, alpha, beta):
        # Agent index always 0
        agentIndex = 0
        bestAction = ('', -float('inf'))
        legalActions = gameState.getLegalActions(agentIndex)
            
        for action in legalActions:
            nextGameState = gameState.generateSuccessor(agentIndex, action)

            score = self.alphabeta(nextGameState, depth + 1, alpha, beta)
            maxScore = bestAction[1]
            if (score > maxScore):
                maxScore = score
                bestAction = (action, maxScore)
                
            # Prunning condition
            if (maxScore > beta):
                return bestAction

            alpha = max(score, alpha)
        
        return bestAction

    # Return min value
    def minValue(self, gameState, depth, agentIndex, alpha, beta):
        legalActions = gameState.getLegalActions(agentIndex)
        minScore = float('inf')

        for action in legalActions:
            nextGameState = gameState.generateSuccessor(agentIndex, action)

            score = self.alphabeta(nextGameState, depth + 1, alpha, beta)
            if (score < minScore):
                minScore = score

            # Prunning condition
            if (minScore < alpha):
                return minScore

            beta = min(minScore, beta)
        
        return minScore

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
        return self.maxValue(gameState, 0)[0]
        util.raiseNotDefined()

    def expectimax(self, gameState, depth):
        if depth == self.depth * gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        
        agentIndex = depth % gameState.getNumAgents()
        
        if agentIndex == 0:
            return self.maxValue(gameState, depth)[1]

        return self.expValue(gameState, depth, agentIndex)

    def maxValue(self, gameState, depth):
        # Agent index always 0
        agentIndex = 0
        bestAction = ('', -float('inf'))
        legalActions = gameState.getLegalActions(agentIndex)
            
        for action in legalActions:
            nextGameState = gameState.generateSuccessor(agentIndex, action)

            score = self.expectimax(nextGameState, depth + 1)
            if (score > bestAction[1]):
                bestAction = (action, score)
        
        return bestAction

    def expValue(self, gameState, depth, agentIndex):
        legalActions = gameState.getLegalActions(agentIndex)
        totalScore = 0

        for action in legalActions:
            nextGameState = gameState.generateSuccessor(agentIndex, action) 
            totalScore += self.expectimax(nextGameState, depth + 1)
        
        bestScore = float(totalScore)/float(len(legalActions))
        
        return bestScore

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    pos = currentGameState.getPacmanPosition()

    foodList = currentGameState.getFood().asList()
    foodLeft = len(foodList)

    pelletList = currentGameState.getCapsules()
    pelletLeft = len(pelletList)

    ghostList = currentGameState.getGhostStates()
    scaredGhostDists = []
    activeGhostDists = []

    # Ghost
    for ghost in ghostList:
        ghostDist = manhattanDistance(pos, ghost.getPosition())
        if ghost.scaredTimer is not 0:
            scaredGhostDists.append(ghostDist)
        else:
            activeGhostDists.append(ghostDist)

    if len(scaredGhostDists) > 0:
        closestGhost = min(scaredGhostDists)
        score -= 3 * closestGhost
    
    if len(activeGhostDists) > 0:
        closestGhost = min(activeGhostDists)
        score += closestGhost

    # Food
    if (foodLeft > 0):
        foodDistances = [ util.manhattanDistance(pos, food) for food in foodList]
        closestFood = min(foodDistances)
        score -= closestFood

    score -= 30 * pelletLeft
    score -= 4 * foodLeft

    return score 
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

