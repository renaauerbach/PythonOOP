#
# board.py (Final project)
#
# A Board class for the Eight Puzzle
#
# name: Rena Auerbach   
# email: renaauer@bu.edu
#
# If you worked with a partner, put his or her contact info below:
# partner's name:
# partner's email:
#

class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[0] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1

        # Put your code for the rest of __init__ below.
        # Do *NOT* remove our code above.
        x = 0
        for row in range(len(self.tiles[0])):
            for col in range(len(self.tiles)):
                self.tiles[row][col] = int(digitstr[x])
                x += 1
                if self.tiles[row][col] == 0:
                    self.blank_r = row
                    self.blank_c = col

    ### Add your other method definitions below. ###
    def __repr__(self):
        """returns a string representation of a Board object"""
        string = ''
        for row in range(len(self.tiles[0])):
            for col in range(len(self.tiles)):               
                if self.tiles[row][col] == 0:
                    string += '-' + ' '
                else:
                    string += str(self.tiles[row][col]) + ' '
            string += '\n'

        return string


    def move_blank(self, direction):
        """attempts to modify the contents of the called Board object according
        to the specifies direction input. if the move is possible, the call
        returns True, otherwise returns False
        """
        empty_r = self.blank_r
        empty_c = self.blank_c
        old_blank = self.tiles[self.blank_r][self.blank_c]
        
        if direction == 'up':
            empty_r -= 1
        elif direction == 'down':
            empty_r += 1
        elif direction == 'left':
            empty_c -= 1
        elif direction == 'right':
            empty_c += 1
        else:
            print('unknown direction:', direction)
            return False

        if empty_r in range(len(self.tiles[0])) and empty_c in range(len(self.tiles)):
            self.tiles[self.blank_r][self.blank_c] = self.tiles[empty_r][empty_c]
            self.tiles[empty_r][empty_c] = 0
            self.blank_r = empty_r
            self.blank_c = empty_c
            return True
        else:
            return False


    def digit_string(self):
        """creates and returns a string of digits that corresponds to the
        current contents of the called Board object’s tiles attribute
        """
        string = ''
        for row in range(len(self.tiles[0])):
            for col in range(len(self.tiles)):
                string += str(self.tiles[row][col])
        return string


    def copy(self):
        """returns a newly-constructed Board object that is a deep copy
        of the called object
        """
        new_board = Board(self.digit_string())
        return new_board


    def num_misplaced(self):
        """counts and returns the number of tiles in the called Board object
        that are not where they should be in the goal state
        """
        num = 0
        if self.tiles[0][1] != 1:
            num += 1
        if self.tiles[0][2] != 2:
            num += 1
        if self.tiles[1][0] != 3:
            num += 1
        if self.tiles[1][1] != 4:
            num += 1
        if self.tiles[1][2] != 5:
            num += 1
        if self.tiles[2][0] != 6:
            num += 1
        if self.tiles[2][1] != 7:
            num += 1
        if self.tiles[2][2] != 8:
            num += 1

        return num


    def __eq__(self, other):
        """return True if the called object (self) and the argument (other)
        have the same values for the tiles attribute, otherwise returns False
        """
        if self.tiles == other.tiles:
            return True
        else:
            return False
        
### Added method for h2 ###
    def solver(self):
        """comptues and returns the Manhattan distance between the indices
        of each number in the current state and their respective desired indices
        in the goal state
        """
        goal = [[0, 1, 2],
                [3, 4, 5],
                [6, 7, 8]]
        diff = 0
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[0])):
                val = self.tiles[row][col]
                if goal[row][col] == val:
                    diff += 0
                else:
                    for x in range(len(goal)):
                        for y in range(len(goal[0])):
                            if goal[x][y] == val:
                                x_goal = x
                                y_goal = y
                                diff += (abs(col - y_goal) + abs(row - x_goal))
        return diff

        
            
            
