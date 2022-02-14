from a_star import astar
from bfs import bfs


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


if __name__ == '__main__':
    while True:
        set_number = int(input("Enter 0 ~ 9 for different puzzle sets (-1 to exit): "))
        if set_number == -1:
            print("\n\tSearch terminated. Play again next time.\n")
            break
        elif set_number not in range(10):
            print("\n\tInvalid puzzle set! Please try again.\n")
        else:
            stt = State(set_number)
            print("\nSearching Strategy: A* Searching Algorithm")
            astar(stt.i_state, stt.g_state)
            print("Searching Strategy: Breadth-First Search Searching Algorithm")
            bfs(stt.i_state, stt.g_state)

    stop = input("Press enter to terminate the program.")
