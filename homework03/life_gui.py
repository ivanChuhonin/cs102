import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.screen = pygame.display.set_mode((life.rows * cell_size, life.cols * cell_size))
        self.cell_size = cell_size
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.life.rows):
            xp = self.cell_size * x
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (xp, 0),
                (xp, self.life.cols * self.cell_size),
            )
        for y in range(0, self.life.cols):
            yp = self.cell_size * y
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (0, yp),
                (self.life.rows * self.cell_size, yp),
            )
        pass

    def draw_grid(self) -> None:
        y = 0
        for line in self.life.curr_generation:
            x = 0
            for item in line:
                color = pygame.Color("green") if item == 1 else pygame.Color("white")
                rect = [
                    1 + y * self.cell_size,
                    1 + x * self.cell_size,
                    self.cell_size - 1,
                    self.cell_size - 1,
                ]
                pygame.draw.rect(self.screen, color, rect)
                x += 1
            y += 1
        pass

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            if (
                self.life.curr_generation == self.life.max_generations
                or self.life.is_changing is False
            ):
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)

            self.life.prev_generation = self.life.curr_generation
            self.life.curr_generation = self.life.get_next_generation()

        pygame.quit()
        pass


if __name__ == "__main__":
    game = GameOfLife((15, 10), max_generations=50)
    ui = GUI(game)
    ui.run()
