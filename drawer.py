import curses


class Drawer():
    def __init__(self, scr, items):
        self.scr = scr
        self.cursor = (0, 0)
        self.display_cursor = (0, 0)
        self.view = (0,0)
        self.items = items
        self.PADWIDTH = 1000
        self.PADHEIGHT = 1000
        self.pad = curses.newpad(self.PADHEIGHT, self.PADWIDTH)
        self.height, self.width = scr.getmaxyx()
        self.maxs = []

    def update_cursor(self, dy, dx):
        cy, cx = self.cursor
        cy, cx = (cy + dy, cx + dx)
        cy = max(0, min(self.PADHEIGHT, cy))
        cx = max(0, min(self.PADWIDTH, cx))
        dcy, dcx = self.display_cursor
        dcy, dcx = (dcy + dy, dcx + dx)
        h, w = self.height-1, self.width-1
        vy, vx = self.view
        if dcy > h or dcy < 0:
            dcy = dcy - dy
            vy = vy + dy
        if dcx > w or dcx < 0:
            dcx = dcx - dx
            vx = vx + dx

        self.cursor = (cy, cx)
        self.display_cursor = (dcy, dcx)
        self.view = (vy, vx)

    def get_max(self):
        maxs = [len(str(x)) for x in self.items[0]]
        for item in self.items:
            for i, v in enumerate(item):
                if len(str(v)) > maxs[i]:
                    maxs[i] = len(str(v))
        self.maxs = maxs

    def draw_items(self):
        (self.height, self.width) = self.scr.getmaxyx()
        line = 0
        padding = 1
        for item in self.items:
            (p, fn, fp, ln, c, l, t, d) = zip(item, self.maxs)
            
            colors = [curses.color_pair(x) for x in [2, 6, 1, 4, 7]]

            offset = 0        
            self.pad.addstr(line, offset, t[0], colors[0])
            offset += t[1] + padding
            self.pad.addstr(line, offset, fn[0], colors[1])
            offset += len(fn[0])
            self.pad.addstr(line, offset, ':', colors[2])
            offset += 1
            self.pad.addstr(line, offset, str(ln[0]), colors[3])
            offset += ln[1] + fn[1] - len(fn[0]) + padding
            self.pad.addstr(line, offset, str(d[0]), colors[4])
            offset += d[1] + padding
            line += 1
        
        self.pad.move(*self.display_cursor)
        self.scr.refresh()
        self.pad.refresh(self.view[0], self.view[1], 0, 0, self.height-1, self.width-1)

