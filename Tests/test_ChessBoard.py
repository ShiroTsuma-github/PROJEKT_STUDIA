import sys, os
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Modules.ChessBoard import ChessBoard

c = ChessBoard(500)
#NOTE: Not sure why when doing this i made it 0-8, since it gives 9 positions but it looks like I accounted for it
#when working, so I will leave it be for the moment.
def test_ConvertToAiPos():
    assert c.ConvertToAiPos(0, 5) == 'a3'
    assert c.ConvertToAiPos(0, 0) == 'a8'
    assert c.ConvertToAiPos(0, 8) == 'a0'
    assert c.ConvertToAiPos(7, 0) == 'h8'
    assert c.ConvertToAiPos(7, 8) == 'h0'
    with pytest.raises(ValueError):
        c.ConvertToAiPos(8, 8)
#same here
def test_ConvertToDisp():
    assert c.ConvertToDisp('a3') == (0, 5)
    assert c.ConvertToDisp('a8') == (0, 0)
    assert c.ConvertToDisp('a0') == (0, 8)
    assert c.ConvertToDisp('h8') == (7, 0)
    assert c.ConvertToDisp('h0') == (7, 8)
    with pytest.raises(ValueError):
        c.ConvertToDisp('8a')