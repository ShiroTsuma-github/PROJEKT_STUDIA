from chess import *
board = Board()
moves = board.get_moves(1)

print(board)
for pos in moves:
    print(str(pos[0].piece)[-2:])