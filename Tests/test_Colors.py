#   Handling import weirdness
import sys, os
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#   Imports
from Modules.Colors import Colors, WrongInputType

c = Colors()


def test_GetColor():
    assert c.GetColor('black') == (0, 0, 0)
    assert c.GetColor('black', rgb=False) == '#000000'
    with pytest.raises(ValueError) as wi:
        c.GetColor('asdas')
    assert "Color 'asdas'" in str(wi) 
    with pytest.raises(ValueError) as wi:
        c.GetColor('asdadasdas', rgb=False) is None


def test_repr():
    assert type(repr(c)) == str


def test_ToHex():
    assert c.ToHex((255, 255, 255)) == '#FFFFFF'
    assert c.ToHex((0, 0, 0)) == '#000000'
    assert c.ToHex((255, 0, 0)) == '#FF0000'
    assert c.ToHex((0, 255, 0)) == '#00FF00'
    assert c.ToHex((0, 0, 255)) == '#0000FF'
    assert c.ToHex((255, 0, 255)) == '#FF00FF'
    assert c.ToHex((128, 127, 122)) == '#807F7A'
    with pytest.raises(WrongInputType) as wi:
        c.ToHex((260, 260, 260))
    assert 'Color not matching HEX standard' in str(wi)
    with pytest.raises(WrongInputType) as wi:
        c.ToHex((-220, -220, -220))
    assert 'Color not matching HEX standard' in str(wi)


def test_ToRGB():
    assert c.ToRGB('#ffFFff') == (255, 255, 255)
    assert c.ToRGB('#fffF00') == (255, 255, 0)
    assert c.ToRGB('#ff0000') == (255, 0, 0)
    assert c.ToRGB('#0000FF') == (0, 0, 255)
    with pytest.raises(WrongInputType) as wi:
        c.ToRGB('#0000g0')
    assert 'Field outside of range' in str(wi)


def test__str():
    assert len(str(c)) > 1


def test__iter():
    for pos in c:
        assert len(pos) > 1


def test_len():
    assert len(c) == 139


def test_RandomColor():
    for val in c.RandomColor():
        assert val in range(0, 256)
    assert len(c.RandomColor()) == 3


def test_IsCorrectFormat():
    assert c._Colors__IsCorrectFormat('') is False
    assert c._Colors__IsCorrectFormat({}) is False
    assert c._Colors__IsCorrectFormat(()) is False
    assert c._Colors__IsCorrectFormat(11) is False
    assert c._Colors__IsCorrectFormat((11, 5)) is False
    assert c._Colors__IsCorrectFormat((11, 5, -5)) is False
    assert c._Colors__IsCorrectFormat((11, 'adam', '-5')) is False
    assert c._Colors__IsCorrectFormat('#aabbccqweqweqew') is False
    assert c._Colors__IsCorrectFormat('aabbcc') is False
    assert c._Colors__IsCorrectFormat('#aabbcc') is True
    assert c._Colors__IsCorrectFormat((212, 52, 6)) is True
    assert c._Colors__IsCorrectFormat([212, 52, 6]) is True


def test_IsCorrectType():
    assert c._Colors__IsCorrectType((), 'RGB') is True
    assert c._Colors__IsCorrectType([], 'RGB') is True
    assert c._Colors__IsCorrectType('', 'HEX') is True
    assert c._Colors__IsCorrectType(12, 'RGB') is False
    assert c._Colors__IsCorrectType([], 'HEX') is False
    with pytest.raises(WrongInputType) as wi:
        c._Colors__IsCorrectType(5, 'CMYK')
    assert 'Type could not match to HEX|RGB' in str(wi)


def test_IsFullyCorrect():
    assert c.IsFullyCorrect((), 'RGB') is False
    assert c.IsFullyCorrect((), 'HEX') is False
    assert c.IsFullyCorrect(12, 'RGB') is False
    assert c.IsFullyCorrect('dsaasdd', 'HEX') is False
    assert c.IsFullyCorrect('dsaasdd', 'RGB') is False
    assert c.IsFullyCorrect('#aabbcc', 'HEX') is True
    assert c.IsFullyCorrect((200, 50, 12), 'RGB') is True
    assert c.IsFullyCorrect([200, 50, 12], 'RGB') is True
    with pytest.raises(WrongInputType) as wi:
        c.IsFullyCorrect((-200, 22, 13), 'CMYK')
    assert 'Type could not match to HEX|RGB' in str(wi)


def test_ColoredText():
    assert 'Background : NONE' in str(c.ColoredText('test', debug=True))
    assert 'Foreground : #AABBCC' in str(c.ColoredText('test', text_color='#aabbcc', debug=True))
    assert 'Foreground : #FF0000' in str(c.ColoredText('test', text_color=(255, 0, 0), debug=True))
    assert 'Foreground : #FF0000' in str(c.ColoredText('test',
                                                       text_color=(255, 0, 0),
                                                       background_color='#aabbcc',
                                                       debug=True))
    assert 'Background : #AABBCC' in str(c.ColoredText('test',
                                                       text_color=(255, 0, 0),
                                                       background_color='#aabbcc',
                                                       debug=True))
    assert c.ColoredText('Tekst 12', background_color=(255, 255, 255)) == 'Tekst 12'
    assert c.ColoredText('Tekst 12') == 'Tekst 12'
    with pytest.raises(WrongInputType) as wi:
        c.ColoredText('Tekst 12', text_color='asdsaddsads') == 'Tekst 12'
    assert 'Could not match to any color' in str(wi)
    with pytest.raises(WrongInputType) as wi:
        c.ColoredText('Tekst 12', background_color='asdsasdads') == 'Tekst 12'
    assert 'Could not match to any color' in str(wi)


def test_ErrorStr():
    assert str(WrongInputType('Test', 'Testing')) == 'Test : Testing'
