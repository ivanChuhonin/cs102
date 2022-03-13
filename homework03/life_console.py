import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)


    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        line0 = '+' + '-' * self.life.cols + '+'
        line1 = '|' + ' ' * self.life.cols + '|'
        screen.addstr(0, 0, line0)
        for x in range(self.life.rows):
            screen.addstr(x+1, 0, line1)
        screen.addstr(self.life.rows+1, 0, line0)
        pass

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for x in range(self.life.rows):
            items = self.life.curr_generation[x]
            line1 = '|' + ''.join([str(' ' if i == 0 else '*') for i in items]) + '|'
            screen.addstr(x+1, 0, line1)
        # screen.getch()
        screen.refresh()
        pass

    def run(self) -> None:
        screen = curses.initscr()
        screen.clear()
        self.draw_borders(screen)
        self.draw_grid(screen)
        running = True
        while running:
            if self.life.curr_generation == self.life.max_generations or \
                    self.life.is_changing == False:
                running = False
            time.sleep(1)
            self.life.prev_generation = self.life.curr_generation
            self.life.curr_generation = self.life.get_next_generation()
            self.draw_grid(screen)

        curses.endwin()

if __name__ == '__main__':
    game = GameOfLife((5, 80), max_generations=50)
    ui = Console(game)
    ui.run()
