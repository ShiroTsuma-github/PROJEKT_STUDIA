from .Piece import Piece
import pygame
from chess import Board as cbo
from chess import Pawn, Rook, Bishop, King, Queen, Knight, locate


class ChessBoard():
    def __init__(self, size) -> None:
        self.size = size
        self.CellSize = self.size / 8
        self.Positions = self.GeneratePositions()
        self.Pieces = pygame.sprite.Group()
        self.whiteMove = True
        self.MoveLog = []
        self.board = []
        self.ChessAIBoard = cbo(True)

    def GeneratePositions(self, debug=False) -> 'list[tuple[float, float]]':
        """Since board is taken as image instead of generating,
        there is a need for general positions where to place figures.
        `debug` allows for visualising positions.

        Args:
            debug (bool, optional): If visualization is needed. Defaults to False.

        Returns:
            list[tuple[float, float]]: Positions of centers of cells.
        """
        cellWidth = self.CellSize
        debugSize = (15, 15)
        positions = []
        for i in range(8):
            for j in range(8):
                cellX = 5 + cellWidth * j + cellWidth / 2 - j
                cellY = cellWidth * i + cellWidth / 2 - i
                rect = pygame.Rect((0, 0), debugSize)
                positions.append((cellX, cellY))
                if debug:
                    rect.center = (cellX, cellY)
                    pygame.draw.rect(self.screen,
                                     (i * 11, j * 11, abs(j - i) * 15),
                                     rect)
        return positions

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

    def ConvertPos(self, posY, posX) -> str:
        dictX = {0: 'a',
                    1: 'b',
                    2: 'c',
                    3: 'd',
                    4: 'e',
                    5: 'f',
                    6: 'g',
                    7: 'h'}
        return f'{dictX.get(posY)}{8 - (posX)}'

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
                fpos = self.ConvertPos(j, i)
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

    def Move(self, startPos, endPos):
        start = self.ConvertPos(startPos[0], startPos[1])
        end = self.ConvertPos(endPos[0], endPos[1])
        ans = False
        self.ConvertBoard()
        piece1 = self.ChessAIBoard.get_piece(locate(start))
        if piece1 is None:
            return False
        ans = piece1.is_valid(locate(end), self.ChessAIBoard)
        if ans and self.ValidTurn(piece1):
            self.board[endPos[1]][endPos[0]] = self.board[startPos[1]][startPos[0]]
            self.board[startPos[1]][startPos[0]] = '-'
        return ans


"""
 >>> pawn3 = board.get_piece(locate("c7"))
        >>> pawn1.is_valid(locate("d3"), board) # Advance white pawn
        True
        >>> pawn1.is_valid(locate("d4"), board)
"""
