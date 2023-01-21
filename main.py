from Modules.Screen import Screen
play = True
mode = 0
size = 800
while play:
    game = Screen(size)
    game.debug = False
    game.mode = mode
    play, size, mode = game.run(starting_seq='rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR', whiteMove=True)


# TODO:
#en passant - tu not sure xD
#castling - chyba jest wbudowane w make_move ale trzeba sprawdzic
# dodac mozliwosc zmiany rozmiaru okna
# dodac zmiane konfiguracji startowej