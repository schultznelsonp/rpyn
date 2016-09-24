from random import randint
from asciimatics.screen import Screen

def clear_screen(screen):
    for i in range(screen.height):
        screen.move(0, i)
        screen.draw(screen.width, i, char=' ')
        

def demo(screen):
    string = ''
    while True:
        clear_screen(screen)
        screen.print_at(string,
                        screen.width - len(string), 25,
                        colour=7,
                        bg=0)
        ev = screen.get_key()

        if ev in range(0x30, 0x40):
            string += chr(ev)

        elif ev == -300:
            string = string[:-1]

        elif ev in (ord('Q'), ord('q')):
            return

        elif ev == None:
            pass

        else:
            string += str(ev)

        screen.refresh()

Screen.wrapper(demo)
