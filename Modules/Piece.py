import pygame
from .ImageFix import ImageHandle


class Piece(pygame.sprite.Sprite):
    def __init__(self, imgpath, center, size) -> None:
        super().__init__()
        self.base = self.Fix(imgpath, size)
        self.image = self.base.GetImage()
        self.rect = pygame.Rect((0, 0), self.base.GetSize())
        self.rect.center = center

    def Fix(self, imgpath, size):
        temp = ImageHandle(imgpath)
        temp.resize(size / temp.GetSize()[0])
        return temp
