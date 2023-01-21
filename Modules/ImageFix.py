import pygame
from PIL import Image
import sys
import os


def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename


class ImageHandle():
    def __init__(self, imagePath) -> None:
        self.image = Image.open(get_path(imagePath))
        self.surface = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)

    def resize(self, scale) -> None:
        width, height = self.surface.get_size()
        n_w = int(width * scale)
        n_h = int(height * scale)
        self.surface = pygame.transform.scale(self.surface, (n_w, n_h))

    def GetImage(self):
        return self.surface

    def GetSize(self):
        return self.surface.get_size()
