import copy


class Node:
    """ A node class for A* Pathfinding. """

    def __init__(self, parent=None, puzzle_board=None):
        self.parent = parent
        self.puzzle_board = copy.deepcopy(puzzle_board)

        self.g = 0
        self.h = 0
        self.f = 0

    def find_empty_cell(self):
        for row in range(len(self.puzzle_board)):
            for col in range(len(self.puzzle_board[row])):
                if self.puzzle_board[row][col] == 0:
                    return row, col
        return -1, -1

    def make_new_nodes(self):
        adjacent_squares = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        r, c = self.find_empty_cell()
        if r == -1 or c == -1:
            return None

        new_nodes = []
        for pos in adjacent_squares:
            new_pos = (r + pos[0], c + pos[1])
            if (new_pos[0] > (len(self.puzzle_board) - 1) or
                    new_pos[0] < 0 or
                    new_pos[1] > (len(self.puzzle_board[len(self.puzzle_board) - 1]) - 1) or
                    new_pos[1] < 0):
                continue
            new_node = copy.deepcopy(self.puzzle_board)
            new_node[r][c], new_node[new_pos[0]][new_pos[1]] = new_node[new_pos[0]][new_pos[1]], new_node[r][c]
            new_nodes.append(new_node)

        return new_nodes

    def __repr__(self):
        puzzle_board = ""
        for row in self.puzzle_board:
            for cell in row:
                puzzle_board += f"{cell or '_'} "
            puzzle_board += "\n"
        return f"{puzzle_board}--------\ng: {self.g} , h: {self.h} , f: {self.f}\n"

    def __eq__(self, other):
        for row in range(len(self.puzzle_board)):
            for col in range(len(self.puzzle_board[row])):
                if self.puzzle_board[row][col] != other.puzzle_board[row][col]:
                    return False
        return True


class AStar:
    def __init__(self, puzzle_board, end):
        self.puzzle_board = copy.deepcopy(puzzle_board)
        self.end = end

    @staticmethod
    def return_path(current_node):
        """ return Finded path from start to end. """
        path = []
        current = current_node
        while current is not None:
            path.append(current)
            current = current.parent
        # Return reversed path
        return path[::-1]

    def heuristic(self, current_node):
        h = 0
        for row in range(len(self.end)):
            for col in range(len(self.end[row])):
                if current_node[row][col] != self.end[row][col]:
                    h += 1
        return h

    def astar(self):
        """
            Returns a list of tuples as a path
            from the given start to the given end in the given maze
        """

        # Create start and end node
        start_node = Node(None, self.puzzle_board)
        start_node.g = 0
        start_node.h = 0
        start_node.f = 0

        end_node = Node(None, self.end)
        end_node.g = 0
        end_node.h = 0
        end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        iter = 0
        # Loop until you find the end
        while len(open_list) > 0:
            iter += 1
            # if iter > 5:
            #     break
            # print(iter, "*"*20)
            # for idx, item in enumerate(open_list):
            #     print(idx)
            #     print(item)
            if iter % 10 == 0:
                print(".", end="")
            if iter % 1000 == 0:
                print(f"\n{iter} , {len(open_list)}")

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
            if current_node == end_node:
                return self.return_path(current_node)

            # Generate children
            children = []
            new_nodes = current_node.make_new_nodes()
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
                child.h = self.heuristic(child.puzzle_board)
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

        print("Couldn't get a path to destination")
        return None


def main():
    """
        Main method.
        Initiate maze and run A*.
    """
    puzzle_board = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
    end = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    astar = AStar(puzzle_board, end)
    path = astar.astar()

    if path is not None:
        for idx, item in enumerate(path):
            print(idx)
            print(item)


if __name__ == '__main__':
    main()
