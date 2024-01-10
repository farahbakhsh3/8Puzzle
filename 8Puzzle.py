import copy


class Node:
    """ A node class for A* """

    def __init__(self, parent=None, puzzle_board=None):
        self.parent = parent
        self.puzzle_board = copy.deepcopy(puzzle_board)

        self.g = 0
        self.h = 0
        self.f = 0

    def find_empty_cell(self):
        """ Find an empty cell on the puzzle board """
        for row in range(len(self.puzzle_board)):
            for col in range(len(self.puzzle_board[row])):
                if self.puzzle_board[row][col] == 0:
                    return row, col
        return -1, -1

    def make_new_puzzle_boards(self):
        """Make lsit of new puzzle boards based on empty cell """
        adjacent_squares = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        r, c = self.find_empty_cell()
        if r == -1 or c == -1:
            return None

        new_puzzle_boards = []
        for pos in adjacent_squares:
            new_pos = (r + pos[0], c + pos[1])
            if (new_pos[0] > (len(self.puzzle_board) - 1) or
                    new_pos[0] < 0 or
                    new_pos[1] > (len(self.puzzle_board[len(self.puzzle_board) - 1]) - 1) or
                    new_pos[1] < 0):
                continue
            new_puzzle_board = copy.deepcopy(self.puzzle_board)
            new_puzzle_board[r][c], new_puzzle_board[new_pos[0]][new_pos[1]] = (
                new_puzzle_board[new_pos[0]][new_pos[1]], new_puzzle_board[r][c])
            new_puzzle_boards.append(new_puzzle_board)

        return new_puzzle_boards

    def __repr__(self):
        puzzle_board = ""
        for row in self.puzzle_board:
            for cell in row:
                puzzle_board += f"{cell or '_'} "
            puzzle_board += "\n"
        return f"{puzzle_board}--------\ng: {self.g} , h: {self.h} , f: {self.f}\n{'-'*20}\n"

    def __eq__(self, other):
        for row in range(len(self.puzzle_board)):
            for col in range(len(self.puzzle_board[row])):
                if self.puzzle_board[row][col] != other.puzzle_board[row][col]:
                    return False
        return True


class AStar:
    def __init__(self, puzzle_board, goal_board, heurestic_func_name="misplaced"):
        self.puzzle_board = copy.deepcopy(puzzle_board)
        self.goal_board = goal_board

        # Set heurestic function
        self.heurestic = self.heurestic_func(heurestic_func_name)

    @staticmethod
    def return_path(current_node):
        """ return Finded steps from current puzzle board to goal puzzle board """
        steps = []
        current = current_node
        while current is not None:
            steps.append(current)
            current = current.parent
        # Return reversed steps
        return steps[::-1]

    def manhattan_distance(self, puzzle_board):
        """ calculate the manhattan distance between current puzzle board and goal puzzle board. """
        distance = 0
        size = len(puzzle_board)

        for i in range(size):
            for j in range(size):
                if puzzle_board[i][j] != 0:
                    value = puzzle_board[i][j]
                    goal_position = self.find_position(self.goal_board, value)
                    distance += abs(i - goal_position[0]) + abs(j - goal_position[1])

        return distance

    @staticmethod
    def find_position(puzzle_board, value):
        """ find position of value in puzzle board. """
        for i in range(len(puzzle_board)):
            for j in range(len(puzzle_board[i])):
                if puzzle_board[i][j] == value:
                    return i, j

    def misplaced(self, puzzle_board):
        """ calculate the misplaced value between current puzzle_board and goal puzzle board."""
        h = 0
        for row in range(len(self.goal_board)):
            for col in range(len(self.goal_board[row])):
                if puzzle_board[row][col] != self.goal_board[row][col]:
                    h += 1
        return h

    def heurestic_func(self, heurestic_func_name):
        if heurestic_func_name == "manhattan_distance":
            return self.manhattan_distance
        elif heurestic_func_name == "misplaced":
            return self.misplaced
        else:
            AssertionError("Wrong heurestic_func_name")

    def astar(self):
        """
            Returns a list of tuples as a steps
            from the given puzzle board to the given goal puzzle board.
        """
        # Create start and goal node
        start_node = Node(None, self.puzzle_board)
        start_node.g = 0
        start_node.h = 0
        start_node.f = 0

        goal_node = Node(None, self.goal_board)
        goal_node.g = 0
        goal_node.h = 0
        goal_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        idx_iter = 0
        # Loop until you find the goal
        while len(open_list) > 0:
            idx_iter += 1
            if idx_iter % 10 == 0:
                print(".", end="")
            if idx_iter % 1000 == 0:
                print(f"\n{idx_iter} , {len(open_list)}")

            # Get the current node (a node with smallest f)
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == goal_node:
                return self.return_path(current_node)

            # Generate children
            children = []
            new_nodes = current_node.make_new_puzzle_boards()
            for new_node in new_nodes:
                # Create new node
                children.append(Node(current_node, new_node))

            # Loop through children
            for child in children:
                # Child is on the closed list
                _continue = False
                for closed_child in closed_list:
                    if closed_child == child:
                        _continue = True
                if _continue:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = self.heurestic(child.puzzle_board)
                child.f = child.g + child.h

                # Child is already in the open list
                _continue = False
                for open_node in open_list:
                    if (child == open_node
                            and child.g >= open_node.g):
                        _continue = True
                if _continue:
                    continue

                # Add the child to the open list
                open_list.append(child)

        print("There is no solution for this puzzle!!! :-(")
        return None


def main():
    """
        Main method.
        Initiate puzzle board and goal board
        Then run A*.
    """
    puzzle_board = [[4, 7, 2],
                    [6, 8, 5],
                    [3, 1, 0]]
    goal_board = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]]

    astar = AStar(puzzle_board, goal_board, "manhattan_distance")
    steps = astar.astar()

    if steps is not None:
        for idx, item in enumerate(steps):
            print(f"->> Step : {idx} <<-")
            print(item)


if __name__ == '__main__':
    main()
