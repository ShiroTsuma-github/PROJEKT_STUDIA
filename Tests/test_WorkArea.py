import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from main import WorkArea


def test_Init():
    t = WorkArea((0.1, 0.1), (15, 11), (0.3, 0.7))
    assert t.width == 15
    assert t.height == 11
    assert t.PlayableArea == (0.1 * t.width, 0.1 * t.height)

def test_center():
    t = WorkArea((0.45, 0.65), (100, 100), (0.7, 0.3), (0.15, 0.85))
    assert t.center == (61, 37.75)

