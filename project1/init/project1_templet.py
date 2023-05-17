import copy

import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


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
        empty = np.where(chessboard == COLOR_NONE)
        for i in range(len(empty[0])):
            coo_x = empty[0][i]
            coo_y = empty[1][i]
            isValid = self.isValidPos(chessboard, coo_x, coo_y)
            if isValid:
                self.candidate_list.append((coo_x, coo_y))

    def isValidPos(self, chessboard, coo_x, coo_y):
        isValid = False
        # up
        if coo_x > 0:
            tmp = 1
            while (coo_x - tmp) > 0 and chessboard[coo_x - tmp][coo_y] == -self.color:
                tmp += 1
                if chessboard[coo_x - tmp][coo_y] == self.color:
                    isValid = True
                    break
        # down
        if coo_x < self.chessboard_size - 1:
            tmp = 1
            while (coo_x + tmp) < self.chessboard_size - 1 and chessboard[coo_x + tmp][coo_y] == -self.color:
                tmp += 1
                if chessboard[coo_x + tmp][coo_y] == self.color:
                    isValid = True
                    break
        # left
        if coo_y > 0:
            tmp = 1
            while (coo_y - tmp) > 0 and chessboard[coo_x][coo_y - tmp] == -self.color:
                tmp += 1
                if chessboard[coo_x][coo_y - tmp] == self.color:
                    isValid = True
                    break
        # right
        if coo_y < self.chessboard_size - 1:
            tmp = 1
            while (coo_y + tmp) < self.chessboard_size - 1 and chessboard[coo_x][coo_y + tmp] == -self.color:
                tmp += 1
                if chessboard[coo_x][coo_y + tmp] == self.color:
                    isValid = True
                    break
        # UL
        if coo_x > 0 and coo_y > 0:
            tmp = 1
            while (coo_x - tmp) > 0 and (coo_y - tmp) > 0 and chessboard[coo_x - tmp][coo_y - tmp] == -self.color:
                tmp += 1
                if chessboard[coo_x - tmp][coo_y - tmp] == self.color:
                    isValid = True
                    break
        # UR
        if coo_x > 0 and (coo_y < self.chessboard_size - 1):
            tmp = 1
            while (coo_x - tmp) > 0 and (coo_y + tmp) < self.chessboard_size - 1 and chessboard[coo_x - tmp][
                coo_y + tmp] == -self.color:
                tmp += 1
                if chessboard[coo_x - tmp][coo_y + tmp] == self.color:
                    isValid = True
                    break
        # DL
        if (coo_x < self.chessboard_size - 1) and coo_y > 0:
            tmp = 1
            while (coo_x + tmp) < self.chessboard_size - 1 and (coo_y - tmp) > 0 and chessboard[coo_x + tmp][
                coo_y - tmp] == -self.color:
                tmp += 1
                if chessboard[coo_x + tmp][coo_y - tmp] == self.color:
                    isValid = True
                    break
        # DR
        if (coo_x < self.chessboard_size - 1) and (coo_y < self.chessboard_size - 1):
            tmp = 1
            while (coo_x + tmp) < self.chessboard_size - 1 and (coo_y + tmp) < self.chessboard_size - 1 and \
                    chessboard[coo_x + tmp][
                        coo_y + tmp] == -self.color:
                tmp += 1
                if chessboard[coo_x + tmp][coo_y + tmp] == self.color:
                    isValid = True
                    break
        return isValid



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
