import pygame
from .ImageFix import ImageHandle


class Screen():
    def __init__(self, size) -> None:
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
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.clock.tick(30)
            pygame.display.flip()

    def getSize(self):
        return self.screen.get_size()
