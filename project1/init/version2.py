import numpy as np
import random
import math
import copy
import time

COLOR_BLACK = -1  # max
COLOR_WHITE = 1  # min
COLOR_NONE = 0
random.seed(0)

Vmap = np.array([[500, -25, 10, 5, 5, 10, -25, 500],
                 [-25, -45, 1, 1, 1, 1, -45, -25],
                 [10, 1, 3, 2, 2, 3, 1, 10],
                 [5, 1, 2, 1, 1, 2, 1, 5],
                 [5, 1, 2, 1, 1, 2, 1, 5],
                 [10, 1, 3, 2, 2, 3, 1, 10],
                 [-25, -45, 1, 1, 1, 1, -45, -25],
                 [500, -25, 10, 5, 5, 10, -25, 500]])

# Vmap = np.array([[-1, 1, 1, -1], [1, 2, 2, 1], [1, 2, 2, 1], [-1, 1, 1, -1]])

dx = [1, 1, 1, -1, -1, -1, 0, 0]
dy = [1, -1, 0, 1, -1, 0, 1, -1]
max_depth = 4


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need to add your decision to your candidate_list. The system will get the end of your candidate_list as
        # your decision.
        self.candidate_list = []

    # The input is the current chessboard. Chessboard is a numpy array.
    def go(self, chessboard):
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        self.candidate_list = self.valid_pos_set(chessboard, self.color)
        if self.color == COLOR_BLACK:
            _, action = self.max_value(chessboard, 0, self.color, -math.inf, math.inf)
            if action is not None:
                self.candidate_list.append(action)
        else:
            _, action = self.min_value(chessboard, 0, self.color, -math.inf, math.inf)
            if action is not None:
                self.candidate_list.append(action)

    def nextState(self, chessboard, action, color):
        nextBoard = copy.deepcopy(chessboard)
        nextBoard[action[0]][action[1]] = color
        for i in range(8):
            a = 1
            while self.chessboard_size > action[0] + a * dx[i] >= 0 and self.chessboard_size > action[1] + a * dy[
                i] >= 0:
                if nextBoard[action[0] + a * dx[i]][action[1] + a * dy[i]] == -color:
                    a += 1
                    if self.chessboard_size > action[0] + a * dx[i] >= 0 and self.chessboard_size > action[1] + a * dy[
                        i] >= 0:
                        if nextBoard[action[0] + a * dx[i]][action[1] + a * dy[i]] == color:
                            for j in range(1, a):
                                nextBoard[action[0] + j * dx[i]][action[1] + j * dy[i]] = color
                            break
                else:
                    break
        return nextBoard

    def curBoardValue(self, chessboard):
        return sum(sum(chessboard * Vmap))

    def max_value(self, chessboard, depth, color, alpha, beta):
        pos_set = self.valid_pos_set(chessboard, color)
        if len(pos_set) == 0 or depth == max_depth:
            return self.curBoardValue(chessboard), None
        v = -math.inf
        move = None
        depth += 1
        for a in pos_set:
            nextBoard = self.nextState(chessboard, a, color)
            v2, _ = self.min_value(nextBoard, depth, -color, alpha, beta)
            if v2 > v:
                v = v2
                move = a
            if v >= beta:
                return v, a
            alpha = max(v, alpha)
        return v, move

    def min_value(self, chessboard, depth, color, alpha, beta):
        pos_set = self.valid_pos_set(chessboard, color)
        if len(pos_set) == 0 or depth == max_depth:
            return self.curBoardValue(chessboard), None
        v = math.inf
        move = None
        depth += 1
        for a in pos_set:
            nextBoard = self.nextState(chessboard, a, color)
            v2, _ = self.max_value(nextBoard, depth, -color, alpha, beta)
            if v2 < v:
                v = v2
                move = a
            if v <= alpha:
                return v, move
            beta = min(beta, v)
        return v, move

    def isValidPos(self, chessboard, coo_x, coo_y, color):
        for i in range(8):
            a = 1
            while self.chessboard_size > coo_x + a * dx[i] >= 0 and self.chessboard_size > coo_y + a * dy[i] >= 0:
                if chessboard[coo_x + a * dx[i]][coo_y + a * dy[i]] == -color:
                    a += 1
                    if self.chessboard_size > coo_x + a * dx[i] >= 0 and self.chessboard_size > coo_y + a * dy[i] >= 0:
                        if chessboard[coo_x + a * dx[i]][coo_y + a * dy[i]] == color:
                            return True
                else:
                    break
        return False

    def valid_pos_set(self, chessboard, color):
        valid_pos_set = []
        empty = np.where(chessboard == COLOR_NONE)
        for i in range(len(empty[0])):
            coo_x = empty[0][i]
            coo_y = empty[1][i]
            isValid = self.isValidPos(chessboard, coo_x, coo_y, color)
            if isValid:
                valid_pos_set.append((coo_x, coo_y))
        return valid_pos_set




# ==============Find new pos========================================
# Make sure that the position of your decision on the chess board is empty.
# If not, the system will return error.
# Add your decision into candidate_list, Records the chessboard
# You need to add all the positions which are valid
# candidate_list example: [(3,3),(4,4)]
# You need append your decision at the end of the candidate_list,
# candidate_list example: [(3,3),(4,4),(4,4)]
# we will pick the last element of the candidate_list as the position you choose.
# In above example, we will pick (4,4) as your decision.
# If there is no valid position, you must return an empty
