from time import sleep
from Modules.Colors import Colors
import pygame


class WorkArea():
    def __init__(self, size: 'tuple[float, float]',
                 WindowSize: 'tuple[int, int]',
                 Xoffsets: 'tuple[float, float]' = (0.5, 0.5),
                 Yoffsets: 'tuple[float, float]' = (0.5, 0.5)) -> None:
        self.width = WindowSize[0]
        self.height = WindowSize[1]
        self.PlayableArea = (self.width * size[0], self.height * size[1])
        self.offsetX = Xoffsets
        self.offsetY = Yoffsets
        self.center = self.__center()
        self.corners = self.__corners()

    def __center(self):
        x_pos = (self.width - self.PlayableArea[0]) * self.offsetX[0] + self.PlayableArea[0] / 2
        y_pos = (self.height - self.PlayableArea[1]) * self.offsetY[0] + self.PlayableArea[1] / 2
        return (x_pos, y_pos)

    def __corners(self):
        return \
            {'lt': (self.center[0] - self.PlayableArea[0] / 2, self.center[1] - self.PlayableArea[1] / 2),
             'lb': (self.center[0] - self.PlayableArea[0] / 2, self.center[1] + self.PlayableArea[1] / 2),
             'rt': (self.center[0] + self.PlayableArea[0] / 2, self.center[1] - self.PlayableArea[1] / 2),
             'rb': (self.center[0] + self.PlayableArea[0] / 2, self.center[1] + self.PlayableArea[1] / 2)}

    def getWidth(self):
        return self.PlayableArea[0]

    def getHeight(self):
        return self.PlayableArea[1]


class ChessBoard(WorkArea):
    def __init__(self,
                 size: 'tuple[float, float]',
                 WindowSize: 'tuple[int, int]',
                 Xoffsets: 'tuple[float, float]' = (0.5, 0.5),
                 Yoffsets: 'tuple[float, float]' = (0.5, 0.5)) -> None:
        super().__init__(size, WindowSize, Xoffsets, Yoffsets)
        self.cellSize = self.PlayableArea[0] / 8
        self.cellList, self.cellColors = self.__generateCellList()

    def __generateCellList(self):
        cells = []
        colors = []
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    colors.append('f1')
                else:
                    colors.append('f2')
                cells.append(pygame.Rect(
                    (self.corners['lt'][0] + j * self.cellSize, self.corners['lt'][1] + i * self.cellSize),
                    (self.cellSize, self.cellSize)))
        return (cells, colors)


class piece(pygame.sprite.Sprite):
    def __init__(self, imgpath, center) -> None:
        super().__init__()
        self.image = pygame.image.load(imgpath)
        self.rect = self.image.get_rect()
        self.rect.center = center


class Window():
    def __init__(self, size: 'tuple[int, int]', chessScale: float = 0.75) -> None:
        self.sizeX = size[0] if type(size[0]) == int else 1000
        self.sizeY = size[1] if type(size[1]) == int else 1000
        self.screen = pygame.display.set_mode((self.sizeX, self.sizeY))
        self.board = ChessBoard((chessScale, chessScale), (self.sizeX, self.sizeY))
        self.boardSize = (self.board.getWidth(), self.board.getHeight())
        self.boardCorners = self.board.corners
        self.pieces = pygame.sprite.Group()

    def start(self, boardColor, cellColor, backgroundColor):
        pygame.init()
        pygame.draw.rect(a.screen, c.GetColor(backgroundColor), ((0, 0), (self.sizeX, self.sizeY)))
        pygame.draw.rect(a.screen,
                         c.GetColor('black'),
                         ((a.boardCorners['lt'][0] - 2, a.boardCorners['lt'][1] - 2),
                          (a.boardSize[0] + 4, a.boardSize[1] + 4)))
        pygame.draw.rect(a.screen, c.GetColor(boardColor), ((a.boardCorners['lt']), (a.boardSize)))
        for poz, i in enumerate(self.board.cellList):
            if self.board.cellColors[poz] == 'f1':
                pygame.draw.rect(self.screen, c.GetColor(cellColor), i)
        self.update()

    def resize(self, size: 'tuple[int, int]'):
        if not all([type(i) for i in size]):
            return
        self.screen = pygame.display.set_mode(size)

    def update(self):
        self.pieces.draw(self.screen)
        pygame.display.flip()

    def drawPieces(self):
        for point in self.board.cellList:
            d = piece('images\Chess_bdt60.png',point.center)
            self.pieces.add(d)


if __name__ == '__main__':
    a = Window((1000, 1000), 0.75)
    c = Colors()
    a.start('white', 'light green', 'light golden rod yellow')
    a.drawPieces()
    a.update()
    while True:
        sleep(5)



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