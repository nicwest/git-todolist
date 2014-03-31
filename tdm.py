import curses
import traceback
import time
import subprocess

from finder import get_list
from drawer import Drawer


def setup():
    curses.setupterm()
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    for x in range(1, 16):
        curses.init_pair(x, x, -1)
    curses.init_pair(16, 1, 4)
    return stdscr


def lookup(drawer):
    items, not_items = get_list('./')
    drawer.items = items
    drawer.get_max()


def draw(drawer):
    drawer.draw_items()


def main(stdscr):
    quitting_time = False
    start_time = time.time()
    last_update = time.time()
    drawer = Drawer(stdscr, [])
    lookup(drawer)
    draw(drawer)
    while not quitting_time:
        c = stdscr.getch()
        t = time.time()

        if t >= last_update + 30.0 or c == ord('r'):
            lookup(drawer)
            draw(drawer)
            last_update = time.time()

        if c == curses.KEY_LEFT:
            drawer.update_cursor(0, -1)
            draw(drawer)

        if c == curses.KEY_RIGHT:
            drawer.update_cursor(0, 1)
            draw(drawer)

        if c == ord('j'):
            drawer.update_cursor(1, 0)
            draw(drawer)

        if c == ord('k'):
            drawer.update_cursor(-1, 0)
            draw(drawer)

        if c == curses.KEY_ENTER:
            item = drawer.items[drawer.cursor[0]]
            subprocess.call(['vim', '+%s' % item[3], item[2]])

        if c == ord('q'):
            quitting_time = True
            continue


def clean_up(stdscr):
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

if __name__ == "__main__":
    stdscr = setup()   # setup curses etc
    try:
        main(stdscr)       # m..m..m.m.MAIN LOOP!
    except:
        clean_up(stdscr)
        traceback.print_exc()
    clean_up(stdscr)   # kill our screen go back to normal
