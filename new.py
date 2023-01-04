from Modules.Screen import Screen
game = Screen(1000)
game.debug = False
game.run(starting_seq='rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR' ,whiteMove=True)


# TODO:
# zdebugowac bo czasami nie ma szachu (przynajmnie nie pisze)
#i zdarzylo ze nie zmienilo pionka a pisal szach
# wtf
# zrobic szach mat
#zrobic promowanie pionkow - sprawdzasz czy po przeciwnej stronie jest pionek
# i jezeli tak to wyswietlasz okno promocji i ponownie generujesz plansze
#en passant - tu not sure xD
#castling - chyba jest wbudowane w make_move ale trzeba sprawdzic
"""))
  File "h:\Dokumenty\GitHub\PROJEKT_STUDIA\env\lib\site-packages\chess\chess.py", line 76, in locate    
    return Position("12345678".index(pos_str[1]), "abcdefgh".index(pos_str[0]))
ValueError: substring not 
found"""
# zrobic sprawdzenie ze jak powyzej 1k pikseli to olewa klik
