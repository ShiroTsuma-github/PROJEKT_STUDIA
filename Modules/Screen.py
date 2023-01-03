import pygame
from .ImageFix import ImageHandle
from .ChessBoard import ChessBoard
from .Colors import Colors


class Screen(ChessBoard):
    def __init__(self, size) -> None:
        super().__init__(size)
        self.size = size
        pygame.init()
        self.screen = pygame.display.set_mode((size + size * 0.12, size))
        self.clock = pygame.time.Clock()
        self.background = self._backgroundResize()
        self._background()

    def _backgroundResize(self):
        temp = ImageHandle('images\\board.png')
        temp.resize(self.size / temp.GetSize()[0])
        return temp

    def _background(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background.GetImage(), (0, 0))

    def BoardMarks(self):
        t = Colors()
        text = pygame.font.SysFont('arial', int(self.size * 10 / 500))
        for i, pos in enumerate(self.Positions):
            tiptextsurface = text.render(self.ConvertPos(i % 8, i // 8).upper(), True, t.GetColor('black'))
            self.screen.blit(tiptextsurface, (pos[0] - self.CellSize / 2.2, pos[1] + self.CellSize / 3))

    def CurrentSelect(self, coords):
        t = Colors()
        print(coords)
        pos = self.Positions[coords[0] + coords[1] * 8 ]
        pygame.draw.circle(self.screen, t.GetColor("red"), pos, self.CellSize * 0.4, width=3)
        print(pos)

    def DisplayScore(self):
        t = Colors()
        text = pygame.font.SysFont('arial', int(self.size * 22 / 500))
        white, black = self.Score()
        whitetextsurface = text.render(str(white), True, t.GetColor('black'))
        blacktextsurface = text.render(str(black), True, t.GetColor('black'))
        self.screen.blit(whitetextsurface, (self.size * 1.035, self.size * 0.85))
        self.screen.blit(blacktextsurface, (self.size * 1.035, self.size * 0.15))

    def DisplayCheck(self):
        t = Colors()
        text = pygame.font.SysFont('arial', int(self.size * 23 / 500))
        print(self.check)
        textsurface = text.render('Check' if self.check else '', True, t.GetColor('black'))
        self.screen.blit(textsurface, (self.size * 1.0, self.size * 0.5))

    def run(self,
            starting_seq='rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR',
            debug=False,
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    mouseX = int(mousePos[0] // (self.size / 8))
                    mouseY = int(mousePos[1] // (self.size / 8))
                    if sqSelected == (mouseX, mouseY):
                        sqSelected = ()
                        clicks = []
                    sqSelected = (mouseX, mouseY)
                    clicks.append(sqSelected) if sqSelected != () else 0
                    if debug:
                        print(F'Y: {mouseY} - X: {mouseX}')
                        print(clicks)
                    if len(clicks) == 1:
                        self.CurrentSelect(clicks[0])
                if len(clicks) == 2:
                    if self.Move(clicks[0], clicks[1]):
                        self.GeneratePieces(self.BoardToPos())
                        if debug:
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
        pygame.display.flip()
