from Modules.Screen import Screen
# game.debug = False
play = True
while play:
    game = Screen(1000)
    game.debug = False
    game.mode = 0
    play = game.run(starting_seq='rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR', whiteMove=True)


# TODO:
#en passant - tu not sure xD
#castling - chyba jest wbudowane w make_move ale trzeba sprawdzic