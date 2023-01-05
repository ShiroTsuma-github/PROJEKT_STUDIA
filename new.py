from Modules.Screen import Screen
# game.debug = False
play = True
while play:
    game = Screen(500)
    game.debug = True
    play = game.run(starting_seq='rnbqkbnr----------------------------------------PPPPPPPPRNBQKBNR', whiteMove=True)


# TODO:
#en passant - tu not sure xD
#castling - chyba jest wbudowane w make_move ale trzeba sprawdzic