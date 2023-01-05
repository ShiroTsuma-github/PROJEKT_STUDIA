import pygame
from .ImageFix import ImageHandle
from .ChessBoard import ChessBoard
from .Colors import Colors


class Screen(ChessBoard):
    def __init__(self, size) -> None:
        super().__init__(size)
        self.size = size
        self.truesize = size + size * 0.12
        pygame.init()
        self.Positions = self.GeneratePositions()
        self.ColorMaster = Colors()
        self.objectcolors = {
            'BLACK': 0,
            'WHITE': 1,
            'WSIDE': self.ColorMaster.GetColor('green'),
            'BSIDE': self.ColorMaster.GetColor('blue'),
            'MARKS': self.ColorMaster.GetColor('black'),
            'BACKGROUND': self.ColorMaster.GetColor('alice blue'),
            'TEXT': self.ColorMaster.GetColor('black'),
            'CHECK': self.ColorMaster.GetColor('red'),
            'CHECKM-B': self.ColorMaster.GetColor('light gray')
        }
        self.screen = pygame.display.set_mode((self.truesize, size))
        self.clock = pygame.time.Clock()
        self.background = self._backgroundResize()
        self._background()

    def _backgroundResize(self):
        temp = ImageHandle('images\\board.png')
        temp.resize(self.size / temp.GetSize()[0])
        return temp

    def _background(self):
        self.screen.fill(self.objectcolors['BACKGROUND'])
        self.screen.blit(self.background.GetImage(), (0, 0))

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

    def BoardMarks(self):
        text = pygame.font.SysFont('calibri', int(self.size * 10 / 500))
        for i, pos in enumerate(self.Positions):
            tiptextsurface = text.render(self.ConvertToAiPos(i % 8, i // 8).upper(),
                                         True,
                                         self.objectcolors['MARKS'])
            self.screen.blit(tiptextsurface, (pos[0] - self.CellSize / 2.2, pos[1] + self.CellSize / 3))

    def CurrentSelect(self, coords):
        if self.debug:
            print(f'Chessboard Coordinates : {coords}')
        color = self.objectcolors['WSIDE'] if self.whiteMove\
            else self.objectcolors['BSIDE']
        pos = self.Positions[coords[0] + coords[1] * 8]
        pygame.draw.circle(self.screen,
                           color,
                           pos,
                           self.CellSize * 0.4,
                           width=3)
        if self.debug:
            print(f'Position of cursor : {pos}')

    def DisplayScore(self):
        text = pygame.font.SysFont('calibri', int(self.size * 22 / 500))
        white, black = self.Score()
        whitetextsurface = text.render(str(white), True, self.objectcolors['TEXT'])
        blacktextsurface = text.render(str(black), True, self.objectcolors['TEXT'])
        self.screen.blit(whitetextsurface, (self.size * 1.035, self.size * 0.85))
        self.screen.blit(blacktextsurface, (self.size * 1.035, self.size * 0.15))

    def DisplayCheck(self):
        p = None
        text = pygame.font.SysFont('calibri', int(self.size * 23 / 500))
        if self.debug:
            print(self.check)
        textsurface = text.render('Check' if self.check else '', True, self.objectcolors['TEXT'])
        self.screen.blit(textsurface, (self.size * 1.0, self.size * 0.5))
        if self.checkSide[0]:
            p = self.IndexOfPiece('K')
        elif self.checkSide[1]:
            p = self.IndexOfPiece('k')
        if p:
            pos = self.Positions[p[0] * 8 + p[1]]
            pygame.draw.circle(self.screen,
                               self.objectcolors['CHECK'],
                               pos,
                               self.CellSize * 0.4,
                               width=3)

    def DisplayCheckMate(self):
        text = pygame.font.SysFont('calibri', int(self.size * 50 / 500))
        textsurface = text.render('Checkmate',
                                  True,
                                  self.objectcolors['TEXT'])
        textarea = pygame.Surface(textsurface.get_size())
        textarea.fill(self.objectcolors['CHECKM-B'])
        x, y = textarea.get_size()
        textarea.blit(textsurface, (0, 0))
        self.screen.blit(textarea,
                         ((self.size - textarea.get_width()) // 2,
                          (self.size - textarea.get_height()) // 2))

    def DisplayAvailable(self, position):
        coords = self.ConvertToDisp(str(position))
        pos = self.Positions[coords[0] + coords[1] * 8]
        color = self.objectcolors['WSIDE'] if self.whiteMove else self.objectcolors['BSIDE']
        pygame.draw.circle(self.screen,
                           color,
                           pos,
                           self.CellSize * 0.1,
                           width=3)

    def run(self,
            starting_seq='rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR',
            whiteMove=True):
        self.GeneratePieces(starting_seq)
        self.update()
        self.whiteMove = whiteMove
        run = True
        sqSelected = ()
        clicks = []
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    mouseX = int(mousePos[0] // (self.size / 8))
                    mouseY = int(mousePos[1] // (self.size / 8))
                    if sqSelected == (mouseX, mouseY):
                        sqSelected = ()
                        clicks = []
                    sqSelected = (mouseX, mouseY)
                    if mousePos[0] > self.size + 25 and mousePos[1] > self.size - 50:
                        return True
                    if any([i >= 8 for i in sqSelected]):
                        sqSelected = ()
                    clicks.append(sqSelected) if sqSelected != () else 0
                    if self.debug:
                        print(F'Y: {mouseY} - X: {mouseX}')
                        print(clicks)
                    if len(clicks) == 1:
                        self.CurrentSelect(clicks[0])
                        moves, all_moves = self.availableMoves(clicks[0])
                        if len(all_moves) == 0:
                            self.checkmate = True
                            continue
                        for pos in moves:
                            self.DisplayAvailable(pos)
                if len(clicks) == 2:
                    if self.Move(clicks[0], clicks[1]):
                        self.GeneratePieces(self.BoardToPos())
                        if self.debug:
                            print("Valid Move")
                            self.ConvertBoard()
                            print(self.ChessAIBoard)
                    clicks = []
                    self.update()
            self.clock.tick(60)
            pygame.display.flip()

    def getSize(self):
        return self.screen.get_size()

    def update(self):
        self._background()
        self.BoardMarks()
        self.Pieces.draw(self.screen)
        self.DisplayScore()
        self.DisplayCheck()
        if self.checkmate:
            self.DisplayCheckMate()
        pygame.display.flip()
