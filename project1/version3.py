import numpy as np
import random
import math
import copy
import time

COLOR_BLACK = -1  # min
COLOR_WHITE = 1  # max
COLOR_NONE = 0
random.seed(0)

Vmap = np.array([[-500, 25, 10, 5, 5, 10, 25, -500],
                 [25, 45, 1, 1, 1, 1, 45, 25],
                 [10, 1, 3, 2, 2, 3, 1, 10],
                 [5, 1, 2, 1, 1, 2, 1, 5],
                 [5, 1, 2, 1, 1, 2, 1, 5],
                 [10, 1, 3, 2, 2, 3, 1, 10],
                 [25, 45, 1, 1, 1, 1, 45, 25],
                 [-500, 25, 10, 5, 5, 10, 25, -500]])

dx = [1, 1, 1, -1, -1, -1, 0, 0]
dy = [1, -1, 0, 1, -1, 0, 1, -1]
max_depth = 6
board_weight = 1
stable_weight = -20
action_weight = 10


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
        global max_depth
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        empty = np.where(chessboard == COLOR_NONE)
        emptyPOS = len(empty[0])
        if emptyPOS >= 57:
            max_depth = 6
        elif emptyPOS <= 25:
            max_depth = 6
        else:
            max_depth = 4
        self.candidate_list, _ = valid_pos_set(self.chessboard_size, chessboard, self.color)
        if self.color == COLOR_BLACK:
            _, action = min_value(self.chessboard_size, chessboard, 0, self.color, -math.inf, math.inf)
            if action is not None:
                self.candidate_list.append(action)
        else:
            _, action = max_value(self.chessboard_size, chessboard, 0, self.color, -math.inf, math.inf)
            if action is not None:
                self.candidate_list.append(action)


def nextState(chessboard_size, chessboard, action, color):
    nextBoard = copy.deepcopy(chessboard)
    nextBoard[action[0]][action[1]] = color
    for i in range(8):
        a = 1
        while chessboard_size > action[0] + a * dx[i] >= 0 and chessboard_size > action[1] + a * dy[
            i] >= 0:
            if nextBoard[action[0] + a * dx[i]][action[1] + a * dy[i]] == -color:
                a += 1
                if chessboard_size > action[0] + a * dx[i] >= 0 and chessboard_size > action[1] + a * dy[
                    i] >= 0:
                    if nextBoard[action[0] + a * dx[i]][action[1] + a * dy[i]] == color:
                        for j in range(1, a):
                            nextBoard[action[0] + j * dx[i]][action[1] + j * dy[i]] = color
                        break
            else:
                break
    return nextBoard


def max_value(chessboard_size, chessboard, depth, color, alpha, beta):
    pos_set, actionAbility = valid_pos_set(chessboard_size, chessboard, color)
    if actionAbility == 0 or depth == max_depth:
        return judgeFuc(chessboard_size, chessboard, color), None
    v = -math.inf
    move = None
    depth += 1
    for a in pos_set:
        nextBoard = nextState(chessboard_size, chessboard, a, color)
        v2, _ = min_value(chessboard_size, nextBoard, depth, -color, alpha, beta)
        if v2 > v:
            v = v2
            move = a
        if v >= beta:
            return v, a
        alpha = max(v, alpha)
    return v, move


def min_value(chessboard_size, chessboard, depth, color, alpha, beta):
    pos_set, actionAbility = valid_pos_set(chessboard_size, chessboard, color)
    if actionAbility == 0 or depth == max_depth:
        return judgeFuc(chessboard_size, chessboard, color), None
    v = math.inf
    move = None
    depth += 1
    for a in pos_set:
        nextBoard = nextState(chessboard_size, chessboard, a, color)
        v2, _ = max_value(chessboard_size, nextBoard, depth, -color, alpha, beta)
        if v2 < v:
            v = v2
            move = a
        if v <= alpha:
            return v, move
        beta = min(beta, v)
    return v, move


def isValidPos(chessboard_size, chessboard, coo_x, coo_y, color):
    for i in range(8):
        a = 1
        while chessboard_size > coo_x + a * dx[i] >= 0 and chessboard_size > coo_y + a * dy[i] >= 0:
            if chessboard[coo_x + a * dx[i]][coo_y + a * dy[i]] == -color:
                a += 1
                if chessboard_size > coo_x + a * dx[i] >= 0 and chessboard_size > coo_y + a * dy[i] >= 0:
                    if chessboard[coo_x + a * dx[i]][coo_y + a * dy[i]] == color:
                        return True
            else:
                break
    return False


# 行动力（越大越好）, 合法位置
def valid_pos_set(chessboard_size, chessboard, color):
    pos_set = []
    empty = np.where(chessboard == COLOR_NONE)
    for i in range(len(empty[0])):
        coo_x = empty[0][i]
        coo_y = empty[1][i]
        isValid = isValidPos(chessboard_size, chessboard, coo_x, coo_y, color)
        if isValid:
            pos_set.append((coo_x, coo_y))
    return pos_set, len(pos_set)


# 棋盘估值（黑棋越小越好，白棋越大越好）
def curBoardValue(chessboard):
    return sum(sum(chessboard * Vmap))


# 稳定子数量（越小越好）
def stableNodeValue(chessboard, color):
    stable = [0, 0, 0]
    # 角, 边, 八个方向都无空格
    find1 = [0, 0, 7, 7]
    find2 = [0, 7, 7, 0]
    inc1 = [0, 1, 0, -1]
    inc2 = [1, 0, -1, 0]
    stop = [0, 0, 0, 0]
    for i in range(4):
        if chessboard[find1[i]][find2[i]] == color:
            stop[i] = 1
            stable[0] += 1
            for j in range(1, 7):
                if chessboard[find1[i] + inc1[i] * j][find2[i] + inc2[i] * j] != color:
                    break
                else:
                    stop[i] = j + 1
                    stable[1] += 1
    for i in range(4):
        if chessboard[find1[i]][find2[i]] == color:
            for j in range(1, 7 - stop[i - 1]):
                if chessboard[find1[i] - inc1[i - 1] * j][find2[i] - inc2[i - 1] * j] != color:
                    break
                else:
                    stable[1] += 1
    colFull = np.zeros((8, 8), dtype=int)
    colFull[:, np.sum(abs(chessboard), axis=0) == 8] = True
    rowFull = np.zeros((8, 8), dtype=int)
    rowFull[np.sum(abs(chessboard), axis=1) == 8, :] = True
    diag1full = np.zeros((8, 8), dtype=int)
    diag2full = np.zeros((8, 8), dtype=int)  # 左上右下对角线
    for i in range(15):  # 右上左下对角线
        diagSum1 = 0
        diagSum2 = 0
        if i <= 7:
            send1 = i
            send2 = 0
            send3 = 7
            jRange = i + 1
        else:
            send1 = 7
            send2 = i - 7
            send3 = 14 - i
            jRange = 15 - i
        for j in range(jRange):
            diagSum1 += abs(chessboard[send1 - j][send2 + j])
            diagSum2 += abs(chessboard[send1 - j][send3 - j])
        if diagSum1 == jRange:
            for j in range(jRange):
                diag1full[send1 - j][send2 + j] = True
        if diagSum2 == jRange:
            for j in range(jRange):
                diag2full[send1 - j][send3 - j] = True
    stable[2] = sum(
        sum(np.logical_and(np.logical_and(np.logical_and(colFull, rowFull), diag1full), diag2full)))
    return sum(stable)


# 奇偶性（如果在对局中棋手都没有跳步，那么黑棋无论何时下棋盘面都会有偶数个空位，而白棋无论何时下棋都是奇数个空位。）
# 正常白棋（易使稳定子增多）是劣势，扭转方法为找到一个黑棋无法下的区域，除去该区域下一步黑棋只有奇数个空位

# 估值函数
def judgeFuc(chessboard_size, chessboard, color):
    boardVal = curBoardValue(chessboard)
    stableValue = stableNodeValue(chessboard, color)
    _, actionAbility = valid_pos_set(chessboard_size, chessboard, color)
    value = board_weight * boardVal + color * ((stable_weight * stableValue) + action_weight * actionAbility)
    return value


# test = AI(8, 1, 5)
# x = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,-1,0,0,0,0],[0,0,0,-1,-1,0,0,0],[0,1,1,-1,1,0,0,
# 0],[0,-1,-1,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
# board = np.array(x)
# start = time.time()
# test.go(board)
# end = time.time()
# print((end - start))
# print(test.candidate_list)

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
