from .Piece import Piece
import pygame
from typing import Union
from chess import Board as cbo
from chess import Pawn, Rook, Bishop, King, Queen, Knight, locate
from chess import ai


class ChessBoard():
    def __init__(self, size) -> None:
        self.size = size
        self.mode = 0  # 0:p-b; 1:b-b; 2:p-p
        self.CellSize = self.size / 8
        self.Pieces = pygame.sprite.Group()
        self.whiteMove = True
        self.MoveLog = []
        self.board = []
        self.ChessAIBoard = cbo(empty=True)
        self.check = False
        self.checkmate = False
        self.checkSide = [False, False]
        self.additionalinfo = [[0, 0, 0], [0, 0, 0]]
        self.debug = False

    def ChangeMode(self):
        self.mode += 1
        if self.mode > 3:
            self.mode = 0
        return self.mode

    def availableMoves(self, position):
        self.ConvertBoard()
        all_moves = list(self.ChessAIBoard.get_moves(0 if self.whiteMove else 1))
        Cposition = self.ConvertToAiPos(position[0], position[1])
        pos_moves = []
        for pos in all_moves:
            move = pos[0]
            where_to = move.position
            who = str(move.piece)[-2:]
            if self.debug:
                print(who, where_to)
            if who == Cposition:
                pos_moves.append(where_to)
        if self.debug:
            print(pos_moves)
        return (pos_moves, all_moves)

    def BestMove(self):
        self.ConvertBoard()
        ans = ai.minimax_with_pruning(self.ChessAIBoard, 10, 0 if self.whiteMove else 1)
        if ans[1] is None:
            return False
        if ans[1].piece.position is None:
            return False
        else:
            return ans

    def GeneratePieces(self, positions: str):
        """Based on `positions` recreates the board. `positions`  is string of length 64.
        It includes Characters prnbqk-PRNBQK representing side and figure.
        Small characters represent black and large white. - means empty space.

        Args:
            positions (int): String of board positions. Length 64
        """
        self.board = []
        self.Pieces = pygame.sprite.Group()
        start_Pos = positions
        if len(positions) != 64:
            raise ValueError
        for poz, i in enumerate(self.Positions):
            if poz % 8 == 0:
                self.board.append([])
            if start_Pos[poz] == '-':
                self.board[poz // 8].append(start_Pos[poz])
                continue
            elif start_Pos[poz].lower() not in 'prnbqk':
                raise ValueError(f"Incorrect figure [{start_Pos[poz]}]")
            self.board[poz // 8].append(start_Pos[poz])
            p = f'{start_Pos[poz].lower()}{1 if start_Pos[poz].islower() else 2}'
            d = Piece(f'images\\{p}.png', i, self.size / 7)
            self.Pieces.add(d)

    def BoardToPos(self) -> str:
        res = ''
        for line in self.board:
            for pos in line:
                res += pos
        return res

    def Score(self):
        return (self.ChessAIBoard.compute_score(0), self.ChessAIBoard.compute_score(1))

    def ConvertToAiPos(self, posY, posX) -> str:
        dictX = {0: 'a',
                    1: 'b',
                    2: 'c',
                    3: 'd',
                    4: 'e',
                    5: 'f',
                    6: 'g',
                    7: 'h'}
        if posX > 8 or posY > 7:
            raise ValueError('Out of bound of board.')
        return f'{dictX.get(posY)}{8 - (posX)}'

    def ConvertToDisp(self, pos):
        dictX = {'a': 0,
                 'b': 1,
                 'c': 2,
                 'd': 3,
                 'e': 4,
                 'f': 5,
                 'g': 6,
                 'h': 7}
        if pos[0] not in 'abcdefgh' or pos[1] not in '012345678':
            raise ValueError('Incorrect field.')
        return (dictX.get(pos[0]), abs(int(pos[1]) - 8))

    def IndexOfPiece(self, piece: str) -> Union["tuple[int, int]", None]:
        for i, x in enumerate(self.board):
            try:
                return (i, x.index(piece))
            except ValueError:
                pass
        return None

    def ConvertBoard(self):
        tempBoard = cbo(empty=True)
        for i, line in enumerate(self.board):
            for j, pos in enumerate(line):
                if pos == '-':
                    continue
                if pos.islower():
                    color = 1
                else:
                    color = 0
                fpos = self.ConvertToAiPos(j, i)
                if pos.lower() == 'r':
                    tempBoard.add_piece(Rook(color, locate(fpos)))  # type: ignore
                elif pos.lower() == 'p':
                    tempBoard.add_piece(Pawn(color, locate(fpos)))  # type: ignore
                elif pos.lower() == 'k':
                    tempBoard.add_piece(King(color, locate(fpos)))  # type: ignore
                elif pos.lower() == 'q':
                    tempBoard.add_piece(Queen(color, locate(fpos)))  # type: ignore
                elif pos.lower() == 'n':
                    tempBoard.add_piece(Knight(color, locate(fpos)))  # type: ignore
                elif pos.lower() == 'b':
                    tempBoard.add_piece(Bishop(color, locate(fpos)))  # type: ignore
        self.ChessAIBoard = tempBoard

    def ValidTurn(self, piece):
        if piece.color == 0 and self.whiteMove is True:
            self.whiteMove = False
            return True
        elif piece.color == 1 and self.whiteMove is False:
            self.whiteMove = True
            return True
        return False

    def Move(self, startPos, endPos, a_con=False):
        if a_con:
            start = startPos
            end = endPos
            startPos = self.ConvertToDisp(start)
            endPos = self.ConvertToDisp(end)
        else:
            start = self.ConvertToAiPos(startPos[0], startPos[1])
            end = self.ConvertToAiPos(endPos[0], endPos[1])
        ans = False
        self.ConvertBoard()
        piece1 = self.ChessAIBoard.get_piece(locate(start))
        if piece1 is None:
            return False
        ans = piece1.is_valid(locate(end), self.ChessAIBoard)
        if ans:
            self.ChessAIBoard.move_piece(piece1, locate(end))
            ans = not self.ChessAIBoard.in_check(0 if self.whiteMove else 1)
        self.checkSide[0] = self.ChessAIBoard.in_check(0)
        self.checkSide[1] = self.ChessAIBoard.in_check(1)
        self.check = any(self.checkSide)
        if ans and self.ValidTurn(piece1):
            self.board[endPos[1]][endPos[0]] = self.board[startPos[1]][startPos[0]]
            self.board[startPos[1]][startPos[0]] = '-'
        if piece1.name == 'pawn':
            if (endPos[1] == 7 and piece1.color == 1):
                self.board[endPos[1]][endPos[0]] = 'q'
            elif (endPos[1] == 0 and piece1.color == 0):
                self.board[endPos[1]][endPos[0]] = 'Q'
        self.ConvertBoard()
        self.checkSide[0] = self.ChessAIBoard.in_check(0)
        self.checkSide[1] = self.ChessAIBoard.in_check(1)
        self.check = any(self.checkSide)
        return ans

"""
    >>> bishop = board.get_piece(locate("c1"))
    >>> bishop.position
    c1
    >>> bishop.name
    'bishop'
    >>> bishop = board.move_piece(bishop, locate("f6"))
    >>> bishop.position
    f6
    >>> board.get_piece(locate("f6")) is bishop
    True
    >>> board.get_piece(locate("c1")) is None
    True
"""