from Modules.Screen import Screen
game = Screen(800)
game.run(debug=True, whiteMove=True)

# TODO:
# zrobic szach mat
# mozliwe ruchy - uzyc generatora ktory dsal koles
#zrobic promowanie pionkow - sprawdzasz czy po przeciwnej stronie jest pionek
# i jezeli tak to wyswietlasz okno promocji i ponownie generujesz plansze
#en passant - tu not sure xD
#castling - chyba jest wbudowane w make_move ale trzeba sprawdzic