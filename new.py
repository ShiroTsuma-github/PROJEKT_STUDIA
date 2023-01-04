from Modules.Screen import Screen
game = Screen(500)
game.debug = False
game.run(starting_seq='rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR', whiteMove=True)


# TODO:
#zrobic promowanie pionkow - sprawdzasz czy po przeciwnej stronie jest pionek (naj;epiej tylko na krolowa)
# i jezeli tak to wyswietlasz okno promocji i ponownie generujesz plansze
#en passant - tu not sure xD
#castling - chyba jest wbudowane w make_move ale trzeba sprawdzic