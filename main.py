from Modules.Screen import Screen
play = True
mode = 0
size = 800
move = True
while play:
    game = Screen(size)
    game.debug = False
    game.mode = mode
    game.whiteStart = move
    play, size, mode, move = game.run(
        starting_seq='rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR',)


# TODO:
#en passant - tu not sure xD
#castling - chyba jest wbudowane w make_move ale trzeba sprawdzic
# dodac mozliwosc zmiany rozmiaru okna
# dodac zmiane konfiguracji startowej



# test case dopisany
# jak wyglada dziedziczenie