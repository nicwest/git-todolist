import curses
import traceback
import time

from finder import get_list
from drawer import Drawer


def setup(debug):
    curses.setupterm()
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    return stdscr, debug


def lookup_and_draw(stdscr, drawer):
    items, not_items = get_list('./test_data')
    drawer.items = items
    drawer.draw_items()


def main(stdscr):
    quitting_time = False
    start_time = time.time()
    last_update = time.time()
    drawer = Drawer(stdscr, [])
    lookup_and_draw(stdscr, drawer)
    while not quitting_time:
        c = stdscr.getch()
        t = time.time()

        if t >= last_update + 30.0 or c == ord('r'):
            lookup_and_draw(stdscr, drawer)
            last_update = time.time()
        
        if c == ord('h'):
            drawer.cursor = (drawer.cursor[0], drawer.cursor[1]-1)
            lookup_and_draw(stdscr, drawer)

        if c == ord('l'):
            drawer.cursor = (drawer.cursor[0], drawer.cursor[1]+1)
            lookup_and_draw(stdscr, drawer)
        
        if c == ord('q'):
            quitting_time = True
            continue


def clean_up(stdscr):
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

if __name__ == "__main__":
    debug = "TROLOLWOLWOLWOL!!!!"
    stdscr, debug = setup(debug)   # setup curses etc
    try:
        main(stdscr)       # m..m..m.m.MAIN LOOP!
    except:
        clean_up(stdscr)
        traceback.print_exc()
    clean_up(stdscr)   # kill our screen go back to normal
    print debug
