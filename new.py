from Modules.Screen import Screen
# game.debug = False
play = True
mode = 0
size = 1000
while play:
    game = Screen(size)
    game.debug = False
    game.mode = mode
    play, size, mode = game.run(starting_seq='rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR', whiteMove=True)


# TODO:
#en passant - tu not sure xD
#castling - chyba jest wbudowane w make_move ale trzeba sprawdzic