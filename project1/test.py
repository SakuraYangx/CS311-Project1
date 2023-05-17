# import version5
# import version6
# import numpy
# import copy
#
# dx = [1, 1, 1, -1, -1, -1, 0, 0]
# dy = [1, -1, 0, 1, -1, 0, 1, -1]
#
#
# def nextState(chessboard_size, chessboard, action, color):
#     nextBoard = copy.deepcopy(chessboard)
#     nextBoard[action[0]][action[1]] = color
#     for i in range(8):
#         a = 1
#         while chessboard_size > action[0] + a * dx[i] >= 0 and chessboard_size > action[1] + a * dy[
#             i] >= 0:
#             if nextBoard[action[0] + a * dx[i]][action[1] + a * dy[i]] == -color:
#                 a += 1
#                 if chessboard_size > action[0] + a * dx[i] >= 0 and chessboard_size > action[1] + a * dy[
#                     i] >= 0:
#                     if nextBoard[action[0] + a * dx[i]][action[1] + a * dy[i]] == color:
#                         for j in range(1, a):
#                             nextBoard[action[0] + j * dx[i]][action[1] + j * dy[i]] = color
#                         break
#             else:
#                 break
#     return nextBoard
#
#
# board = numpy.zeros((8, 8))
# white = version5.AI(8, 1, 5)
# black = version6.AI(8, -1, 5)
# board[3][3] = 1
# board[3][4] = -1
# board[4][3] = -1
# board[4][4] = 1
# empty = numpy.where(board == 0)
# turn = -1
# while len(empty[0]) != 0:
#     if turn == -1:
#         black.go(board)
#         if len(black.candidate_list) == 0:
#             turn = -turn
#             continue
#         choose = black.candidate_list[-1]
#         board = nextState(8, board, choose, -1)
#     else:
#         white.go(board)
#         if len(white.candidate_list) == 0:
#             turn = -turn
#             continue
#         choose = white.candidate_list[-1]
#         board = nextState(8, board, choose, 1)
#     turn = -turn
#     empty = numpy.where(board == 0)
#     print(board)
#
# print(sum(sum(board)))
import random
a = [(0, 0), (1, 2), (3, 2),(7, 0)]
b = []
for i in a:
    if i != (0, 0) and i != (7, 0):
        b.append(i)
print(b)
tmp = random.choice(b)
print(tmp)
index = a.index(tmp)
print(index)