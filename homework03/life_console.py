import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

        self.screen = curses.initscr()

    def draw_borders(self) -> None:
        """Отобразить рамку."""
        self.screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self) -> None:
        """Отобразить состояние клеток."""
        num_rows, num_cols = self.screen.getmaxyx()

        mcol = num_cols // 2 - self.life.cols
        for rowi, row in enumerate(self.life.curr_generation):
            mrow = num_rows // 2 - self.life.rows // 2 + rowi
            line = " ".join((" " if value else "*" for value in row))
            try:
                self.screen.addstr(mrow, mcol, line)
            except curses.error:
                pass

    def run(self) -> None:
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.screen.clear()
            self.draw_borders()
            self.draw_grid()
            self.screen.refresh()
            self.life.step()
            time.sleep(0.1)
        curses.endwin()
