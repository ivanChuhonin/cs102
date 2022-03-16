import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 4
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid: Grid = []

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        y = 0
        for line in self.grid:
            x = 0
            for item in line:
                color = pygame.Color("green") if item == 1 else pygame.Color("white")
                rect = [
                    1 + x * self.cell_size,
                    1 + y * self.cell_size,
                    self.cell_size - 1,
                    self.cell_size - 1,
                ]
                pygame.draw.rect(self.screen, color, rect)
                x += 1
            y += 1

        pass

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        game.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            for h in range(self.cell_height):
                self.grid.append([random.randint(0, 1) for _ in range(self.cell_width)])
        else:
            for h in range(self.cell_height):
                self.grid.append([0 for _ in range(self.cell_width)])

        return self.grid

    def get_neighboursXY(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        (x, y) = cell
        if x > self.cell_width or y > self.cell_height:
            return []

        result = []
        if y == 0:
            line0 = self.grid[0]
            line1 = self.grid[1]
            if x == 0:
                result = line1[0:2]
                result.append(line0[1])
            elif x == self.cell_width - 1:
                result = line1[-2:]
                result.append(line0[x - 1])
            else:
                result = line1[x - 1 : x + 2]
                result.append(line0[x - 1])
                result.append(line0[x + 1])
        elif y == self.cell_height - 1:
            line0 = self.grid[y]
            line1 = self.grid[y - 1]
            if x == 0:
                result = line1[0:2]
                result.append(line0[1])
            elif x == self.cell_width - 1:
                result = line1[-2:]
                result.append(line0[x - 1])
            else:
                result = line1[x - 1 : x + 2]
                result.append(line0[x - 1])
                result.append(line0[x + 1])
        else:
            line0 = self.grid[y]
            line1 = self.grid[y - 1]
            line2 = self.grid[y + 1]
            if x == 0:
                result = line1[0:2] + line2[0:2]
                result.append(line0[1])
            elif x == self.cell_width - 1:
                result = line1[-2:] + line2[-2:]
                result.append(line0[x - 1])
            else:
                result = line1[x - 1 : x + 2] + line2[x - 1 : x + 2]
                result.append(line0[x - 1])
                result.append(line0[x + 1])

        return result

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        (xx, yy) = cell
        if xx > self.cell_height or yy > self.cell_width:
            return []

        result = []
        if xx == 0:
            line0 = self.grid[0]
            line1 = self.grid[1]
            if yy == 0:
                result = line1[0:2]
                result.append(line0[1])
            elif yy == self.cell_width - 1:
                result = line1[-2:]
                result.append(line0[yy - 1])
            else:
                result = line1[yy - 1 : yy + 2]
                result.append(line0[yy - 1])
                result.append(line0[yy + 1])
        elif xx == self.cell_height - 1:
            line0 = self.grid[xx]
            line1 = self.grid[xx - 1]
            if yy == 0:
                result = line1[0:2]
                result.append(line0[1])
            elif yy == self.cell_width - 1:
                result = line1[-2:]
                result.append(line0[yy - 1])
            else:
                result = line1[yy - 1 : yy + 2]
                result.append(line0[yy - 1])
                result.append(line0[yy + 1])
        else:
            line0 = self.grid[xx]
            line1 = self.grid[xx - 1]
            line2 = self.grid[xx + 1]
            if yy == 0:
                result = line1[0:2] + line2[0:2]
                result.append(line0[1])
            elif yy == self.cell_width - 1:
                result = line1[-2:] + line2[-2:]
                result.append(line0[yy - 1])
            else:
                result = line1[yy - 1 : yy + 2] + line2[yy - 1 : yy + 2]
                result.append(line0[yy - 1])
                result.append(line0[yy + 1])

        return result

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        newGrid = []
        y = 0
        for line in self.grid:
            x = 0
            newLine = []
            for item in line:
                countAlife = sum(self.get_neighboursXY((x, y)))
                if item == 1:
                    if countAlife == 2 or countAlife == 3:
                        newLine.append(1)
                    else:
                        newLine.append(0)
                else:
                    if countAlife == 3:
                        newLine.append(1)
                    else:
                        newLine.append(0)
                x += 1
            y += 1
            newGrid.append(newLine)
        self.grid = newGrid
        return newGrid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
