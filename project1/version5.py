import numpy as np
import random
import math
import copy
import time

COLOR_BLACK = -1  # min
COLOR_WHITE = 1  # max
COLOR_NONE = 0
random.seed(0)

Vmap = np.array([[-500, 100, 10, 5, 5, 10, 100, -500],
                 [100, 50, 1, 1, 1, 1, 50, 100],
                 [10, 1, 3, 2, 2, 3, 1, 10],
                 [5, 1, 2, 1, 1, 2, 1, 5],
                 [5, 1, 2, 1, 1, 2, 1, 5],
                 [10, 1, 3, 2, 2, 3, 1, 10],
                 [100, 50, 1, 1, 1, 1, 50, 100],
                 [-500, 100, 10, 5, 5, 10, 100, -500]])

dx = [1, 1, 1, -1, -1, -1, 0, 0]
dy = [1, -1, 0, 1, -1, 0, 1, -1]
max_depth = 4
board_weight = 1
stable_weight = -60
action_weight = 30


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
        if chessboard[0][0] == self.color:
            Vmap[0][1] = -500
            Vmap[1][0] = -500
        if chessboard[0][7] == self.color:
            Vmap[0][6] = -500
            Vmap[1][7] = -500
        if chessboard[7][0] == self.color:
            Vmap[6][0] = -500
            Vmap[7][1] = -500
        if chessboard[7][7] == self.color:
            Vmap[7][6] = -500
            Vmap[6][7] = -500
        for i in range(1, 7):
            if chessboard[0][i] == self.color:
                Vmap[0][i - 1] = -500
                Vmap[0][i + 1] = -500
            if chessboard[7][i] == self.color:
                Vmap[7][i - 1] = -500
                Vmap[7][i + 1] = -500
            if chessboard[i][0] == self.color:
                Vmap[i - 1][0] = -500
                Vmap[i + 1][0] = -500
            if chessboard[0][i] == self.color:
                Vmap[i - 1][7] = -500
                Vmap[i + 1][7] = -500
        self.candidate_list, _ = valid_pos_set(self.chessboard_size, chessboard, self.color)
        if len(self.candidate_list) > 1:
            tmp = self.candidate_list[-1]
            self.candidate_list[-1] = self.candidate_list[-2]
            self.candidate_list[-2] = tmp
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
        return judgeFuc(chessboard_size, chessboard, pos_set, color), None
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
        return judgeFuc(chessboard_size, chessboard, pos_set, color), None
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
def OuterStableNode(chessboard, color):
    stableMap = np.zeros((8, 8))
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
            stableMap[find1[i]][find2[i]] = color
            for j in range(1, 7):
                if chessboard[find1[i] + inc1[i] * j][find2[i] + inc2[i] * j] != color:
                    break
                else:
                    stableMap[find1[i] + inc1[i] * j][find2[i] + inc2[i] * j] = color
                    stop[i] = j + 1
                    stable[1] += 1
    for i in range(4):
        if chessboard[find1[i]][find2[i]] == color:
            for j in range(1, 7 - stop[i - 1]):
                if chessboard[find1[i] - inc1[i - 1] * j][find2[i] - inc2[i - 1] * j] != color:
                    break
                else:
                    stableMap[find1[i] - inc1[i - 1] * j][find2[i] - inc2[i - 1] * j] = color
                    stable[1] += 1
    return stableMap


def StableNode(chessboard, color):
    def checkUPDOWN(x, y):
        if x - 1 == -1 or x + 1 == 8:
            return 1
        elif checkReverse(x - 1, y) == color or MyStableMap[x + 1][y] == color:
            return 1
        elif opStableMap[x - 1][y] == -color and opStableMap[x + 1][y] == -color:
            return 1
        return 0

    def checkLR(x, y):
        if y - 1 == -1 or y + 1 == 8:
            return 1
        elif MyStableMap[x][y - 1] == color or MyStableMap[x][y + 1] == color:
            return 1
        elif opStableMap[x][y - 1] == -color and opStableMap[x][y + 1] == -color:
            return 1
        return 0

    def checkLURD(x, y):
        if x - 1 == -1 or x + 1 == 8 or y - 1 == -1 or y + 1 == 8:
            return 1
        elif MyStableMap[x - 1][y - 1] == color or MyStableMap[x + 1][y + 1] == color:
            return 1
        elif opStableMap[x - 1][y - 1] == -color and opStableMap[x + 1][y + 1] == -color:
            return 1
        return 0

    def checkLDRU(x, y):
        if x - 1 == -1 or x + 1 == 8 or y - 1 == -1 or y + 1 == 8:
            return 1
        elif MyStableMap[x + 1][y - 1] == color or MyStableMap[x - 1][y + 1] == color:
            return 1
        elif opStableMap[x + 1][y - 1] == -color and opStableMap[x - 1][y + 1] == -color:
            return 1
        return 0

    def checkReverse(x, y):
        count = checkUPDOWN(x, y) + checkLR(x, y) + checkLURD(x, y) + checkLDRU(x, y)
        if count == 4:
            return True
        return False

    count = 0
    MyStableMap = OuterStableNode(chessboard, color)
    opStableMap = OuterStableNode(chessboard, -color)
    myChess = np.where(chessboard == color)
    for i in range(len(myChess[0])):
        count += checkReverse(myChess[0][i], myChess[1][i])
    return count


# 奇偶性（如果在对局中棋手都没有跳步，那么黑棋无论何时下棋盘面都会有偶数个空位，而白棋无论何时下棋都是奇数个空位。）
# 正常白棋（易使稳定子增多）是劣势，扭转方法为找到一个黑棋无法下的区域，除去该区域下一步黑棋只有奇数个空位

# 估值函数
def judgeFuc(chessboard_size, chessboard, pos_set, color):
    boardVal = curBoardValue(chessboard)
    stableValue = StableNode(chessboard, -color)
    myActionAbility = len(pos_set)
    if myActionAbility != 0:
        action = pos_set[-1]
        nextBoard = nextState(chessboard_size, chessboard, action, color)
        nexSet = valid_pos_set(chessboard_size, nextBoard, -color)
        opActionability = len(nexSet)
    else:
        nexSet = valid_pos_set(chessboard_size, chessboard, -color)
        opActionability = len(nexSet)
    value = board_weight * boardVal - color * (
            (stable_weight * stableValue) + action_weight * (3 * opActionability - myActionAbility))
    return value


# test = AI(8, -1, 5)
# x = [[0, 0, 1, -1, 0, -1, 1, 0], [-1, 0, 1, 1, -1, -1, -1, 1], [1, 1, 1, 1, 1, -1, -1, 0], [0, 1, 1, 1, 1, -1, -1, 1],
#      [1, 1, -1, -1, -1, -1, -1, 0], [1, 1, -1, -1, -1, -1, 0, -1], [-1, 1, 1, -1, -1, -1, 0, 0], [0, 1, 1, 1, 1, 0, -1, 0]]
# board = np.array(x)
# start = time.time()
# test.go(board)
# end = time.time()
# print((end - start))
# print(test.candidate_list)
