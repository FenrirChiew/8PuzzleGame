# PROJECT NAME          : 8PuzzleGame
# AUTHORS               : CHIEW HONG KUANG
# COURSE                : AACS3273 FUNDAMENTALS OF ARTIFICIAL INTELLIGENT
# PROJECT OBJECTIVES    : Analyze and evaluate performance of AI algorithms in solving 10 sets of 8 Puzzle Game
#                         using two different Searching Algorithms.
import time
import psutil


class State:
    """
    A State class to store all initial states and the goal state of 10 puzzle sets.
    """

    def __init__(self, set_num):
        """
        A constructor of the State object.
        :param set_num: Integer value that represent the Set Number of puzzle set.
        """
        self.i_state = None
        self.initial_state(set_num)
        self.g_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    def initial_state(self, set_num):
        """
        Initialize the Initial State of the puzzle set using a user input Puzzle Set Number.
        :param set_num: Integer value that represent the Puzzle Set Number.
        :return: None.
        """
        # initial state
        state_sheet = [[[8, 2, 1], [3, 7, 4], [6, 0, 5]],
                       [[6, 5, 0], [4, 8, 1], [2, 3, 7]],
                       [[1, 0, 5], [3, 6, 2], [4, 7, 8]],
                       [[3, 0, 7], [2, 8, 1], [6, 4, 5]],
                       [[1, 2, 0], [4, 5, 3], [7, 8, 6]],
                       [[3, 1, 2], [4, 0, 5], [6, 7, 8]],
                       [[8, 0, 5], [1, 3, 7], [6, 4, 2]],
                       [[6, 4, 1], [7, 8, 0], [5, 2, 3]],
                       [[3, 1, 2], [4, 5, 8], [6, 7, 0]],
                       [[1, 2, 3], [0, 4, 6], [7, 5, 8]]]
        self.i_state = state_sheet[set_num]


class Node:
    """
    A Node class that represents a group of data
    after the Parent Node spent a Path Cost and
    perform an Action to achieve a State.
    """

    def __init__(self, state, parent, action, depth):
        """
        A constructor of the Node object.
        :param state: Matrix object that represents the State of puzzle.
        :param parent: Node object that represents the Parent Node.
        :param action: String object that represents the Action of the Parent Node performed.
        ('up' / 'down' / 'left' / 'right').
        :param depth: Integer value that represents the Depth of the Node path.
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.f_n = None

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

    def move(self, x1, y1, x2, y2):
        """
        Performs puzzle's tiles swapping for Tile 1 and Tile 2.
        :param x1: Integer value that represents the Tile 1's X-Coordinate.
        :param y1: Integer value that represents the Tile 1's Y-Coordinate.
        :param x2: Integer value that represents the Tile 2's Y-Coordinate.
        :param y2: Integer value that represents the Tile 2's X-Coordinate.
        :return: A Matrix's Value after swapping.
        """
        state = [x[:] for x in self.state]
        state[x1][y1], state[x2][y2] = state[x2][y2], state[x1][y1]
        return state

    def all_children(self):
        """
        Creates a list of all possible child nodes of the Current State.
        :return: A list of Children.
        """
        x, y = self.search_index_by_tile(0)
        children = []
        # Action: 'up'
        if x != 0:
            children.append(Node(self.move(x, y, x - 1, y), self, 'up', self.depth + 1))
        # Action: 'down'
        if x != len(self.state) - 1:
            children.append(Node(self.move(x, y, x + 1, y), self, 'down', self.depth + 1))
        # Action: 'left'
        if y != 0:
            children.append(Node(self.move(x, y, x, y - 1), self, 'left', self.depth + 1))
        # Action: 'right'
        if y != len(self.state) - 1:
            children.append(Node(self.move(x, y, x, y + 1), self, 'right', self.depth + 1))
        return children

    def draw(self):
        """
        Displays the Node's State of the puzzle set.
        :return: None.
        """
        puzzle = "           "
        for row in self.state:
            for col in row:
                puzzle += str(col) + " "
            puzzle += "\n           "
        print(puzzle)


class PuzzleSet:
    """
    A PuzzleSet class that represents the puzzle set to be solved.
    """

    def __init__(self, init_node, goal_node):
        """
        A constructor of the PuzzleSet object.
        :param init_node: Node object that represents the Initial Node.
        :param goal_node: Node object that represents the Goal Node.
        """
        self.init_node = init_node
        self.goal_node = goal_node
        self.curr_node = self.init_node
        self.frontier_list = []
        self.explored_list = []
        self.path = []

    def manhattan(self, node):
        """
        Finds the sum of the Manhattan Distance of the Current Node (except for the Tile 0).
        :param node: Node object that represent the Current Node.
        :return: The sum of the Manhattan Distance.
        """
        total_distance = 0
        for a in range(len(node.state)):
            for b in range(len(node.state[a])):
                if node.state[a][b] != 0:
                    c, d = self.goal_node.search_index_by_tile(node.state[a][b])
                    total_distance += abs(a - c) + abs(b - d)
        return total_distance

    def f(self, node):
        """
        Sums up Actual Cost to n, g(n) and Estimate
        Cheapest Path Cost, h(n) to find the Estimated
        Lowest Cost Path, f(n).
        :param node: Node object that represent the Goal Node.
        :return:The Estimated Lowest Cost Path, f(n).
        """
        return node.depth + self.manhattan(node)

    def cheapest_frontier_index(self):
        """
        Finds the Index of Node that required minimum cost in the Frontier List.
        :return: The Index of the Cheapest Frontier.
        """
        min_index = 0
        for i in range(len(self.frontier_list)):
            if self.frontier_list[i].f_n < self.frontier_list[min_index].f_n:
                min_index = i
        return min_index

    def in_frontier_list(self, state):
        """
        Finds the Node using given State in the Frontier List.
        :param state: Matrix object that represent the State of Node.
        :return: True if the Node was found; False if none of the Node's State matched the State given.
        """
        for frontier in self.frontier_list:
            if state == frontier.state:
                return True
        return False

    def goal_test(self, state):
        """
        Performs a goal test.
        :param state: Matrix object that represent the Value of Current Node's State.
        :return: The truth for the equality of Current State and Goal State.
        """
        return state == self.goal_node.state

    def solution_path(self, child):
        """
        Tracks the path from the Child Node given until the Root Node is found.
        :param child: Node object that represents the Child Node.
        """
        self.path.append(child)
        while self.path[0].parent is not None:
            self.path.insert(0, self.path[0].parent)

    def solution(self, iterations, start_time, start_memory, child):
        """
        Display the solution of the puzzle set and some statistics.
        :param iterations: Integer value that represents the Iterations of program to find the solution.
        :param start_time: Time object that represents the Start Time.
        :param start_memory: Psutil object that represents the Start Memory.
        :param child: Node object that represents the Child Node.
        :return: True.
        """
        time_used = time.time() - start_time
        memory_used = psutil.Process().memory_info().rss - start_memory

        print("Solution Path:")
        self.solution_path(child)

        print("\n---------------------------\n")
        for node in self.path:
            print("           " + str(node.action).upper())
            node.draw()
            print("---------------------------\n")

        print("Summary of A * Search:")
        print("Total Iterations Used    : " + str(iterations) + " loops")
        print("Total Steps Used         : " + str(len(self.path) - 1) + " steps")
        print("Total Time Used          : " + str(time_used) + " seconds")
        print("Total Memory Used        : " + str(memory_used) + " bytes")
        return True

    def a_star_search(self):
        """
        Performs A * Searching Algorithm to solve the 8-Puzzle Game.
        :return: True if solution was found; False if no solution was found.
        """
        self.frontier_list.append(self.curr_node)
        self.frontier_list[0].f_n = self.f(self.frontier_list[0])

        print("Initial State:\n")
        self.init_node.draw()
        print("Goal State:\n")
        self.goal_node.draw()

        print("Searching will start soon. It might take some time for finding the solution.\n")

        iterations = 1
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        while True:
            if not self.frontier_list:
                print("Puzzle Set Unsolved.\n")
                print("Total Iterations : " + str(iterations) + " loops")
                return False

            self.explored_list.append(self.frontier_list.pop(self.cheapest_frontier_index()))
            for child in self.explored_list[-1].all_children():
                child.f_n = self.f(child)

                if child.state not in self.explored_list and not self.in_frontier_list(child.state):
                    if self.goal_test(child.state):
                        print("Puzzle Set Solved.\n")
                        return self.solution(iterations, start_time, start_memory, child)
                    self.frontier_list.append(child)

            iterations += 1


if __name__ == '__main__':
    while True:
        print("----- INPUT PUZZLE SET -----\n")

        set_number = int(input("Enter 0 ~ 9 for different puzzle sets (-1 to exit): "))
        if set_number == -1:
            print("\n\tSearch terminated. Play again next time.\n")
            break
        elif set_number not in range(10):
            print("\n\tInvalid puzzle set! Please try again.\n")
        else:
            print("\n----- TEST CASE START -----\n")

            # TESTING: PUZZLE SET CREATION
            stt = State(set_number)
            puzzle_set = PuzzleSet(Node(stt.i_state, None, None, 0),
                                   Node(stt.g_state, None, None, 0))

            # TESTING: SEARCHING ALGORITHM
            puzzle_set.a_star_search()

            print("\n----- TEST CASE ENDED -----\n")

    stop = input("Press enter to terminate the program.")
