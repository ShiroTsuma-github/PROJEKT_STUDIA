import pygame
from Modules.Colors import Colors
from Modules.Piece import Piece
from Modules.Screen import Screen





class ChessBoard(Screen):
    def __init__(self, size) -> None:
        super().__init__(size)
        self.Positions = self.GeneratePositions()
        self.Pieces = pygame.sprite.Group()
        self.whiteMove = True
        self.MoveLog = []
        self.board = []

    def GeneratePositions(self, debug=False) -> 'list[tuple[float, float]]':
        """Since board is taken as image instead of generating,
        there is a need for general positions where to place figures.
        `debug` allows for visualising positions.

        Args:
            debug (bool, optional): If visualization is needed. Defaults to False.

        Returns:
            list[tuple[float, float]]: Positions of centers of cells.
        """
        cellWidth = self.size / 8
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

    def update(self):
        self.Pieces.draw(self.screen)
        pygame.display.flip()

    def BoardToPos(self) -> str:
        res = ''
        for line in self.board:
            for pos in line:
                res += pos
        return res


if __name__ == '__main__':
    a = ChessBoard(1000)
    # a.GeneratePositions(debug=True)
    a.GeneratePieces('rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR')
    a.update()
    print(a.board)
    a.run()

# TODO: wygeneruj napodstawie startu tabele 8 x 8, ktora dla kazdej komorki bedzie 
# przechowywac  czy ma pionek, jaki, czyj i moze dostepne ruchy
# na podstawie  dostepnych ruchow pozwalac graczowi na postawienie tam pionka
# zbijanie pionka zbitego, jezeli  jest tam inny
# szach mat