import pygame
from .ImageFix import ImageHandle
from .ChessBoard import ChessBoard


class Screen(ChessBoard):
    def __init__(self, size) -> None:
        super().__init__(size)
        self.size = size
        pygame.init()
        self.screen = pygame.display.set_mode((size, size))
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))
        self.background = self._backgroundResize()
        self.screen.blit(self.background.GetImage(), (0, 0))

    def _backgroundResize(self):
        temp = ImageHandle('images\\board.png')
        temp.resize(self.size / temp.GetSize()[0])
        return temp

    def run(self):
        self.GeneratePieces('qqqqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR')
        run = True
        self.Validate()
        sqSelected = ()
        clicks = []
        while run:
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    mouseX = int(mousePos[0] // (self.size / 8))
                    mouseY = int(mousePos[1] // (self.size / 8))
                    if sqSelected == (mouseY, mouseX):
                        sqSelected = ()
                        clicks = []
                    sqSelected = (mouseY, mouseX)
                    clicks.append(sqSelected)
                    print(F'Y: {mouseY} - X: {mouseX}')
                    print(clicks)
                if len(clicks) == 2:
                    pass           
            self.clock.tick(30)
            pygame.display.flip()

    def getSize(self):
        return self.screen.get_size()

    def update(self):
        self.Pieces.draw(self.screen)
        pygame.display.flip()
