#!/usr/bin/env python
# coding:utf-8

"""
Usage:
$ python3 driver.py <81-digit-board>
$ python3 driver.py   => this assumes a 'sudokus_start.txt'

Saves output to output.txt
"""

import sys
import time
sys.setrecursionlimit(1000000)

start = time.clock()

ROW = "ABCDEFGHI"
COL = "123456789"
TIME_LIMIT = 1.  # max seconds per board
out_filename = 'output.txt'
src_filename = 'sudokus_start.txt'


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def string_to_board(s):
    """
        Helper function to convert a string to board dictionary.
        Scans board L to R, Up to Down.
    """
    return {ROW[r] + COL[c]: int(s[9 * r + c])
            for r in range(9) for c in range(9)}


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def write_solved(board, f_name=out_filename, mode='w+'):
    """
        Solve board and write to desired file, overwriting by default.
        Specify mode='a+' to append.
    """
    result = backtracking(board)
    print(result)  # TODO: Comment out prints when timing runs.
    print()

    # Write board to file
    outfile = open(f_name, mode)
    outfile.write(result)
    outfile.write('\n')
    outfile.close()

    return result


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


def peers(idx):
    squares = cross(ROW, COL)
    unitlist = ([cross(ROW, c) for c in COL] +
                [cross(r, COL) for r in ROW] +
                [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
    units = dict((s, [u for u in unitlist if s in u])
                 for s in squares)
    allpeers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares)
    peers = allpeers[idx]
    return peers

def isConsistent(board, idx, val):
    peer = peers(idx)
    for i in peer:
        if board[i] == val:
            return False
    return True





def restore(domain,remove, val):
    for i in remove:
        domain[i].add(val)
    return domain



def forwardCheck(idx, val, domain, unassigned):
    remove = set()
    length = []
    peer = peers(idx)
    for i in peer:
        if i in unassigned and val in domain[i]:
            remove.add(i)
            length.append(len(domain[i]))
    if 1 in length:
        return False
    for i in remove:
        domain[i].remove(val)
    return [domain,remove]




def mrv(domain, unassigned):
	minIdx, minVal = -1, float('inf')
	for i in unassigned:
		if len(domain[i]) < minVal:
			minVal = len(domain[i])
			minIdx = i
	return minIdx


# def backtrace(board, unassigned, domain):
#     if len(unassigned) == 0:
#         return True
#
#     idx = mrv(domain, unassigned)
#     # print(idx)
#
#     # if board[idx] == 0:
#     for val in domain[idx].copy():
#         if isConsistent(board, idx, val):
#             board[idx] = val
#             unassigned.remove(idx)
#
#             removed = forwardCheck(idx, val, domain, unassigned)
#             if removed == False:
#                 board[idx] = 0
#                 unassigned.add(idx)
#                 continue
#
#             if backtrace(board, unassigned, domain):
#                 return True
#
#             restore(domain, removed)
#             board[idx] = 0
#             unassigned.add(idx)
#         return False
#
#     else:
#         return backtrace(board, unassigned, domain)


def backtrace(board, unassigned, domain):
    if len(unassigned) == 0:
        return board
    idx = mrv(domain, unassigned)
    temp = domain[idx]
    # print(idx)
    for val in domain[idx].copy():
        if isConsistent(board, idx, val):
            board[idx] = val
            unassigned.remove(idx)
            domain[idx] = {val}
            fc = forwardCheck(idx, val, domain, unassigned)
            if fc != False:
                domain = fc[0]
                board_solved = backtrace(board, unassigned, domain)
                if board_solved != False:
                    return board_solved
                restore(domain, fc[1],val)

            board[idx] = 0
            unassigned.add(idx)
            domain[idx] = temp
    return False

# def makeDomain(board, idx):
#     domain = {}
#     if board[idx] != 0:
#         domain[idx] = set([board[idx]])
#     else:
#         domain[idx] = set(range(1, 10))
#     print(domain)
#
#     if board[idx] != 0:
#         for j in peers(idx):
#             print(j,domain[j],board[idx])
#             if len(domain[j]) != 1 and board[idx] in domain[j]:
#                 domain[j].remove(board[idx])


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    boardkey = set(board.keys())
    unassigned = boardkey.copy()
    for i in boardkey:
        if board[i] != 0:
            unassigned.remove(i)

    domain = {}
    for i in boardkey:
        if board[i] != 0:
            domain[i] = set([board[i]])
        else:
            domain[i] = set(range(1, 10))

    for i in board:
        if board[i] != 0:
            for j in peers(i):
                if len(domain[j])!= 1 and board[i] in domain[j]:
                    domain[j].remove(board[i])

    # print("domain:")
    # print(domain)
    # print("unassinged:")
    # print(unassigned)
    board = backtrace(board, unassigned, domain)
    # print(board)
    solved_board = board_to_string(board)
    # time.sleep(5.)
    return solved_board


if __name__ == '__main__':

    if len(sys.argv) > 1:  # Run a single board, as done during grading
        board = string_to_board(sys.argv[1])
        # print(board)
        write_solved(board)
        elapsed = (time.clock() - start)
        print("Time used:", elapsed)

    else:
        print("Running all from sudokus_start")

        #  Read boards from source.
        try:
            srcfile = open(src_filename, "r")
            # print(src_filename)
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Solve each board using backtracking
        solvedNumber = 0
        solvedBoards = []
        count = 0
        for line in sudoku_list.split("\n"):
            start1 = time.clock()
            if len(line) < 9:
                continue

            # Parse boards to dict representation
            board = string_to_board(line)
            # print_board(board)  # TODO: Comment this out when timing runs.

            # Append solved board to output.txt
            write_solved(board, mode='a+')
            elapsed1 = (time.clock() - start1)
            if elapsed1 < 60:
                solvedNumber += 1
                solvedBoards.append(count)
            print("Time used for line %d:" % count, elapsed1)
            count+=1
        print("number of boards which could be solved:", solvedNumber)
        print("Finished all boards in file.")