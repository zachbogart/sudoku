# -*- coding: utf-8 -*-
"""sudoku3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jKBYvYAS692ijQshICYtdPC_pDQewkAy
"""

###############################################################################
#
# Sudoku Solver
#
# Zach Bogart, Max Torke
# 07/2018
#
# Sudoku Solver/Editor made with Python
#
###############################################################################


###############################################################################
# IMPORTS
###############################################################################

import numpy as np


###############################################################################
# PUZZLE BOARDS
###############################################################################

# hard
puzzle_comp_2018 = np.array([[0,3,0,0,4,0,0,0,0],
                         [0,0,5,1,0,0,0,8,9],
                         [0,0,0,0,0,2,7,0,0],
                         [0,0,0,9,1,0,0,0,0],
                         [0,9,4,0,0,0,3,6,0],
                         [0,0,0,0,2,3,0,0,0],
                         [0,0,6,8,0,0,0,0,0],
                         [8,2,0,0,0,9,4,0,0],
                         [0,0,0,0,5,0,0,1,0]])

puzzle_comp_2017 = np.array([[0,9,0,0,0,2,0,0,3],
                             [0,0,2,0,5,0,0,9,0],
                             [0,0,0,3,0,0,7,0,0],
                             [5,0,0,9,0,0,8,0,0],
                             [0,3,0,0,0,0,0,2,0],
                             [0,0,1,0,0,8,0,0,4],
                             [0,0,4,0,0,1,0,0,0],
                             [0,6,0,0,9,0,2,0,0],
                             [1,0,0,8,0,0,0,5,0]])

# easy
puzzle_online_easy = np.array([[0,3,2,0,9,1,0,5,4],
                         [0,0,0,0,0,0,0,0,3],
                         [1,5,0,3,4,0,9,0,7],
                         [0,0,4,0,0,7,0,8,9],
                         [3,2,0,0,6,0,0,0,1],
                         [9,0,1,0,0,0,0,0,0],
                         [4,0,0,6,0,0,7,0,2],
                         [0,0,0,2,0,3,0,0,0],
                         [0,8,0,0,1,4,0,0,5]])

# solved
puzzle_testing_solved = np.array([[8,3,2,7,9,1,6,5,4],
                         [7,4,9,5,2,6,8,1,3],
                         [1,5,6,3,4,8,9,2,7],
                         [5,6,4,1,3,7,2,8,9],
                         [3,2,8,4,6,9,5,7,1],
                         [9,7,1,8,5,2,4,3,6],
                         [4,1,3,6,8,5,7,9,2],
                         [6,9,5,2,7,3,1,4,8],
                         [2,8,7,9,1,4,3,6,5]])

# broken
puzzle_testing_too_many_nines = np.array([[0,3,2,0,9,1,0,5,4],
                         [0,9,0,0,0,0,9,0,3],
                         [1,5,0,3,4,0,9,0,7],
                         [0,0,4,0,0,7,0,8,9],
                         [3,2,0,0,6,0,0,0,1],
                         [9,0,1,0,0,0,0,0,0],
                         [4,0,0,6,0,0,7,0,2],
                         [0,0,0,2,0,3,9,0,0],
                         [0,9,0,0,1,4,0,0,5]])


###############################################################################
# CLASSES
###############################################################################

class SudokuBoard:
    '''
        Defines the sudoku board object
    '''

    # define board and newest addition info
    def __init__(self, board):
        self.board = board
        self.newest_number_row = None
        self.newest_number_col = None

    # print board to screen
    def display(self):
        for row in range(9):
            #Draw horizontal line between each set of 3 numbers in columns
            if row % 3 == 0:
                print ("-------------------------")

            print ("|", end='')
            #Add rows of numbers
            for column in range(9):
                if(self.board[row, column] != 0):
                    # color the newest number so it stands out
                    if self.newest_number_row == row and self.newest_number_col == column:
                        print('\033[95m' + " " + str(self.board[row, column]) + '\033[0m', end='')
                    # normal color
                    else:
                        print(" " + str(self.board[row, column]), end='')
                else:
                    print(" -", end='')
            #Draw vertical lines between each set of 3 numbers in rows
                if (column%3 == 2):
                    print (" |", end='')
            print ("")
        print ("-------------------------\n")

        return

    # get access to board
    def get_board(self):
        return self.board

    # get box values for desired cell
    def get_box_values(self, cell_row, cell_col):
        '''
            returns all cell values in a given cell's square
        '''
        box_coord_row = cell_row//3
        box_coord_col = cell_col//3

        box_vals = []
        for box_pos_row in range(3):
            for box_pos_col in range(3):
                coord_row = 3*box_coord_row + box_pos_row
                coord_col = 3*box_coord_col + box_pos_col
                value = self.board[coord_row][coord_col]
                if (value != 0):
                    box_vals.append(value)

        return box_vals

    # get row values for desired cell
    def get_row_values(self, row):
        '''
            returns all cell values in a given row
        '''
        RowVals = list(self.board[row,:])

    #     print ("RowValues:  " + str(RowVals))
        return RowVals

    # get col values for desired cell
    def get_col_values(self, col):
        '''
            returns all cell values in a given column
        '''

        ColumnVals = list(self.board[:,col])

    #     print ("ColumnValues:  " + str(ColumnVals))
        return ColumnVals

    # get cell value
    def get_cell_value(self, row, col):
        return self.board[row, col]

    # checks board is valid (no duplicates)
    def is_board_valid(self):
        '''
            Checks board is a valid starting board
            - Subroutine for is_board_finished to check end state
        '''
        # check about duplicates
        def there_are_duplicates(nums):
            return len(set(nums)) != len(nums)

        cooordinates = range(9)
        boxes = [[1,1], [1,4], [1,7],
                 [4,1], [4,4], [4,7],
                 [7,1], [7,4], [7,7]]
        digits = range(1,10)

        # check boxes
        for box in boxes:
            # get box values from board
            nums = self.get_box_values(box[0], box[1])
            # check about duplicates
            if there_are_duplicates(nums):
                print('\033[91m' + " " + "Error: Duplicate Detected in a Box (>_<)" + '\033[0m')
                return False

        # check rows
        for row in cooordinates:
            # get row values from board, removing blanks
            nums = self.get_row_values(row)
            nums[:] = [x for x in nums if x != 0]
            # check about duplicates
            if there_are_duplicates(nums):
                print('\033[91m' + " " + "Error: Duplicate Detected in a Row (>_<)" + '\033[0m')
                return False

        # check cols
        for col in cooordinates:
            # get col values from board
            nums = self.get_col_values(col)
            nums[:] = [x for x in nums if x != 0]
            # check about duplicates
            if there_are_duplicates(nums):
                print('\033[91m' + " " + "Error: Duplicate Detected in a Column (>_<)" + '\033[0m')
                return False

        # got all the way with no faults, so done
        return True

    # check if board is finished (no blanks AND no duplicates)
    def is_board_finished(self):
        '''
            Checks board is validly solved (no blanks and no duplicates)
        '''
        # dumb check for no blanks
        if 0 in self.board:
            return False

        return self.is_board_valid()

    # set value for selected cell
    def set_cell_value(self, row, col, val):
        self.board[row, col] = val

    # set value of most recently added number
    def set_newest_number_values(self, row, col):
        self.newest_number_row = row
        self.newest_number_col = col

class CellOptions:
    '''
        Defines the options for every cell on board
    '''

    # define options
    def __init__(self, sudoku_board):

        '''
            create large array of possibilities for every cell
        '''

        # fill value array
        options = np.zeros((9,9,9), dtype=int)
        options[:] = [1,2,3,4,5,6,7,8,9]

        for row in range(9):
            for col in range(9):
                # if cell is decided,remove all other values
                current_val = sudoku_board[row,col]
                if current_val != 0:
                    options[row,col,:current_val-1] = 0
                    options[row,col,current_val:] = 0

        self.options = options

    # print out all options
    def display(self):
        print(self.options)

    # returns options for desired cell
    def get_options_for_cell(self, row, col):
        return self.options[row, col][self.options[row, col] != 0]

    # returns options for desired row
    def get_row_options_array(self, row):
        return self.options[row, :][self.options[row, :] != 0]

    # returns options for desired column
    def get_col_options_array(self, col):
        return self.options[:,col][self.options[:,col] != 0]

    # returns options for desired box
    def get_box_options_array(self, cell_row, cell_col):
        box_coord_row = cell_row//3
        box_coord_col = cell_col//3

        box_options = np.zeros(1, dtype=int)
        for box_pos_row in range(3):
            for box_pos_col in range(3):
                coord_row = 3*box_coord_row + box_pos_row
                coord_col = 3*box_coord_col + box_pos_col
                newvals = self.get_options_for_cell(coord_row,coord_col)
                box_options = np.append(box_options,newvals)

        return box_options[box_options != 0]



    def newfunc(choices, sudoku): # determine which cells contain the only possibility of a certain number inside a row, column, or box

        # for row in range(9):
        #     # count the number of options for each col in a row
        #     option_counts_row = np.count_nonzero(np.tranpose(choices.get_row_options_array(row)), minlength=10)
        #     option_counts_row = np.delete(option_counts, 0)
        #     for col in range(9): # option_counts contains
        #         if option_counts_row[col] == 1 and (sudoku(row,col) != col+1)
        #             # SOLVED A NEW VALUE


        for col in range(9):
            # count the number of options for each row in a col
            array_trans = np.transpose(choices.get_col_options_array(col))
            option_counts_col = np.count_nonzero(array_trans)
            # option_counts_col = np.delete(option_counts, 0)
            for find_indx in range(9):
                if option_counts_col[find_indx] == 1:
                    # find position in array_trans that contains the lone value
                    row = np.argmax(option_counts_col[find_indx])
                    if sudoku(row,col) != find_indx+1:
                        add_number_to_board(cell_row, cell_col, sudoku, choices)
                        return 2, True, (cell_row, cell_col)




        # for box_num in range(9):
        #     row = (box_num%3)*3 # equal to [0,3,6,0,3,6,0,3,6]
        #     col = (box_num//3)*2 # equal to [0,0,0,3,3,3,6,6,6]
        #         np.count_nonzero(np.transpose(get_box_options_array(choices,row,col)), minlength=10)
        #         option_counts_box = np.delete(option_counts, 0)
        #         for iter in range(9):
        #             if option_counts_box[]


    # returns number of options for desired cell
    def get_num_options_for_cell(self, row, col):
        # return len(self.options[row, col])
        return np.count_nonzero(self.options[row, col])

    # remove option from desired cell
    def remove_option_for_cell(self, row, col, val):
        self.options[row, col, val-1] = 0


###############################################################################
# ANALYSIS METHODS
###############################################################################

# checks if one number remains in CellOptions
def only_one_number_left(cell_row, cell_col, choices):
    return choices.get_num_options_for_cell(cell_row, cell_col) == 1

# updates the board object with addition + syntax highlighting for printing
def add_number_to_board(cell_row, cell_col, sudoku, choices):
        # add number to board
        new_number = int(choices.get_options_for_cell(cell_row, cell_col))
        sudoku.set_cell_value(cell_row, cell_col, new_number)

        # make this value bold for printing
        sudoku.set_newest_number_values(cell_row, cell_col)

def immediate_neighbor_elimination(choices, sudoku):
    '''
        update possible values for every cell
        using dumb immediate elimination
            - look at the row, col, and box the cell is in
            - rule out those possibilities
            - if done to one, add to board

        Return:
            - return_code:
                0: no progress
                1: reduced options, no board placement
                2: reduced options + board placement
            - made_progress:
                True: removed possibilities/placed number on board
                False: nothing reduced/placed
            - location:
                (cell_row, cell_col): tuple of newest number addition to board
    '''
    # flag for choices
    choices_removed = 0

    # loop thru all cells
    for cell_row in range(9):
        for cell_col in range(9):

            # if the cell is not defined yet...
            if sudoku.get_cell_value(cell_row, cell_col) == 0:

                # get all neighbors by row/col/box
                box = sudoku.get_box_values(cell_row,cell_col)
                col = sudoku.get_col_values(cell_col)
                row = sudoku.get_row_values(cell_row)
                # combine neighbors to unique list
                all_three = np.array(row + col + box)

                all_three = list(np.unique(all_three))

                # remove current cell value from the group
                all_three.remove(sudoku.get_cell_value(cell_row, cell_col))

                # remove possibilites
                for rmv_num in all_three:
                    # if it's still an option, remove it
                    if rmv_num in choices.get_options_for_cell(cell_row, cell_col):
                        choices.remove_option_for_cell(cell_row, cell_col, rmv_num)
                        choices_removed += 1
                        # if down to only one choice, add it to the board and return
                        if only_one_number_left(cell_row, cell_col, choices):
                            add_number_to_board(cell_row, cell_col, sudoku, choices)
                            return 2, True, (cell_row, cell_col)

    # at this point, nothing was added to board

    # if removed any choices, report progress was made
    if choices_removed > 0:
        return 1, True, None
    # otherwise, say no progress was made
    else:
        return 0, False, None

###############################################################################
# USER STATUS-UPDATE
###############################################################################

# give wordy result for user output
def write_cell_location_in_words(location):
    words = {
        0: "First",
        1: "Second",
        2: "Third",
        3: "Fourth",
        4: "Fifth",
        5: "Sixth",
        6: "Seventh",
        7: "Eighth",
        8: "Ninth"
    }
    return words[location[0]], words[location[1]]

# give user update on what was changed
def respond_to_return_code(code, analysis_type, sudoku, location):
    if code == 0:
        print(analysis_type + ": No progress made (._.)")
    elif code == 1:
        print(analysis_type + ": Removed Possibilities ('_')")
    elif code == 2:
        row, col = write_cell_location_in_words(location)
        print(analysis_type + ": Added a number (^_^)" + "\n  " + str(row) + " Row, " + str(col) + " Column")
        sudoku.display()

        if sudoku.is_board_finished():
            print('\033[92m' + " " + "\nSOLVED ＼(^o^)／" + '\033[0m')
            # display board
            sudoku.newest_number_row, sudoku.newest_number_col = None, None #clear newest number (to avoid highlighting) for final print
            sudoku.display()
            return True


# puzzle_online_easy = np.array([[0,3,2,0,9,1,0,5,4],
#                          [0,0,0,0,0,0,0,0,3],
#                          [1,5,0,3,4,0,9,0,7],
#                          [0,0,4,0,0,7,0,8,9],
#                          [3,2,0,0,6,0,0,0,1],
#                          [9,0,1,0,0,0,0,0,0],
#                          [4,0,0,6,0,0,7,0,2],
#                          [0,0,0,2,0,3,0,0,0],
#                          [0,8,0,0,1,4,0,0,5]])
#
# foo = SudokuBoard(puzzle_online_easy)
# bar = CellOptions(foo.get_board())
#
# # display board initially
# foo.display()
#
# bar.display()
# # bar.get_box_options(0,1)
#
# # bar.get_row_options(0,0)
#
# bar.get_row_options_array(3)

###############################################################################
# MAIN
###############################################################################

def main(board = puzzle_online_easy):

    # setup board and choices objects
    sudoku = SudokuBoard(board)
    options = CellOptions(sudoku.get_board())

    # only solve if board is valid
    if sudoku.is_board_valid():

        # display board initially
        sudoku.display()

        # define flags for progress and return values
        made_progress = True
        return_code = 1

        # define function calls and formatting names
        method_names = {immediate_neighbor_elimination: "Simple Elimination"}
        methods = method_names.keys()

        # while making progress and unsolved, go thru analysis methods
        while made_progress:
            '''
                - 0: no progress made
                - 1: removed possibilities but no num placed
                - 2: num placed on board/removed possibilities
            '''
            # loop thru methods, check if progress is made
            for method in methods:
                # run method
                return_code, made_progress, location = method(options, sudoku)
                # inform user about changes
                if respond_to_return_code(return_code, method_names[method], sudoku, location):
                    return # game finished
                # break if progress was made
                if return_code > 0:
                    break

        # at this point, no progress was made using all methods
        # unable to solve this one
        print('\033[91m' + " " + "\nCould not solve (>_<)" + '\033[0m')
        # display board
        sudoku.newest_number_row, sudoku.newest_number_col = None, None #clear newest number (to avoid highlighting) for final print
        sudoku.display()


if __name__ == "__main__":
    main()
