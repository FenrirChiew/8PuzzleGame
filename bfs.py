# PROJECT NAME          : 8PuzzleGame
# AUTHORS               : KONG ZHI LIN
# COURSE                : AACS3273 FUNDAMENTALS OF ARTIFICIAL INTELLIGENT
# PROJECT OBJECTIVES    : Analyze and evaluate performance of AI algorithms in solving 10 sets of 8 Puzzle Game
#                         using two different Searching Algorithms.
import time
import psutil


# To open a class to store the node (the state, parent node and the action of the puzzle)
class Matrix:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    def search_index_by_tile(self, v):
        """
        Performs index searching of a specified tile's value in a 2D list.
        :param v: Integer value to represent the Value of tile in a 2D list.
        :return: The index of the tile in Row and Column.
        """
        for row in range(len(self.state)):
            for col in range(len(self.state[row])):
                if self.state[row][col] == v:
                    return row, col


class Puzzle:
    def __init__(self, initState, goalState):
        self.initState = initState
        self.goalState = goalState
        self.explored = []
        self.frontier = []
        self.start_time = None
        self.start_memory = None
        self.iterationsUsed = 1

    # Undergo the possible actions (Up, down, Left, Right) from a node state
    def getAction(self, currentNode):
        actions = []  # open a list to store the string list
        x, y = currentNode.search_index_by_tile(0)

        # Action: 'left'
        if y != 0:
            actions.append('Left')
        # Action: 'right'
        if y != len(currentNode.state) - 1:
            actions.append('Right')
        # Action: 'up'
        if x != 0:
            actions.append('Up')
        # Action: 'down'
        if x != len(currentNode.state) - 1:
            actions.append('Down')

        return actions

    # After get the action then the next action will do the changes cells with using swap function
    def swapPuzzle(self, state, x1, y1, x2, y2):
        # Get the puzzle list and use copy function to prevent overwriting the source state
        state = [i[:] for i in state]
        state[x1][y1], state[x2][y2] = state[x2][y2], state[x1][y1]

        return state

        # From the parent's node state and 1 action to return the children node's state

    def nextAction(self, currentNode, action):
        x, y = currentNode.search_index_by_tile(0)

        if action == 'Left':
            return self.swapPuzzle(currentNode.state, x, y, x, y - 1)
        if action == 'Right':
            return self.swapPuzzle(currentNode.state, x, y, x, y + 1)
        if action == 'Up':
            return self.swapPuzzle(currentNode.state, x, y, x - 1, y)
        else:
            return self.swapPuzzle(currentNode.state, x, y, x + 1, y)

    # Display the node state
    def dispalyState(self, state):
        puzzle = ""
        for row in state:
            for col in row:
                puzzle += str(col) + " "
            puzzle += "\n"
        print(puzzle)

    # Pass in the parameter (node's state) if the state is same as the goal state then return true
    def checkGoal(self, state):
        return state == self.goalState

    # If can search the goal state it will record down the information from initial state to goal state
    def solution(self, childNode):
        timeUsed = time.time() - self.start_time
        memoryUsed = psutil.Process().memory_info().rss - self.start_memory

        print("Breadth First Search Success To Find A Solution!\n")
        solutions = [childNode]
        while solutions[0].parent is not None:
            solutions.insert(0, solutions[0].parent)

        depth = 0
        for num in solutions:
            print(num.action)
            self.dispalyState(num.state)
            depth += 1

        print(f"Total Iterations    : {self.iterationsUsed}")
        print(f"Total Steps        : {depth - 1}")
        print(f"Total Time used     : {timeUsed} seconds")
        print(f"Total Storage used  : {memoryUsed}\n")

        return True

    # Use the node state to go through all the nodes in the frontier to check the state is it included in the frontier
    def checkFrontier(self, state):
        for num in self.frontier:
            if state == num.state:
                return True
        return False

    # Breadth First Search Algorithm
    def breadthFirstSearch(self):
        currentNode = Matrix(self.initState, None, None)
        if self.checkGoal(currentNode.state):
            return self.solution(currentNode)

        self.frontier = [currentNode]
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss

        # Output print the initial state
        print("\nInitial State:")
        self.dispalyState(self.initState)
        # Output print the goal state
        print("Goal State:")
        self.dispalyState(self.goalState)

        print("Searching will start soon. It might take some time for finding the solution.\n")

        while True:
            # If the frontier is empty means no solutions found
            if not self.frontier:
                return False

            # let the current node to store the frontier state '0'
            currentNode = self.frontier.pop(0)
            self.explored.append(currentNode.state)
            for action in self.getAction(currentNode):
                child = Matrix(self.nextAction(currentNode, action), currentNode, action)

                # if the child state not occur in explored set and the frontier and also pass the goal test then is a
                # solution.
                if child.state not in self.explored and not self.checkFrontier(child.state):
                    if self.checkGoal(child.state):
                        return self.solution(child)
                    self.frontier.append(child)

            self.iterationsUsed += 1


def bfs(i_state, g_state):
    # declare and initialize the 10 set of goal state
    puzzleGame = Puzzle(i_state, g_state)
    result = puzzleGame.breadthFirstSearch()

    if not result:
        print("Do not found any solutions!!")
        print(f"Total iterations used  : {puzzleGame.iterationsUsed}")
