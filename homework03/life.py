import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self,
            size: tp.Tuple[int, int],
            randomize: bool = True,
            max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        if randomize:
            for h in range(self.rows):
                grid.append([random.randint(0, 1) for _ in range(self.cols)])
        else:
            for h in range(self.rows):
                grid.append([0 for _ in range(self.cols)])

        return grid

    def get_neighboursXY(self, cell: Cell) -> Cells:
        (x, y) = cell
        if x > self.cols or y > self.rows:
            return []

        result = []
        if y == 0:
            line0 = self.curr_generation[0]
            line1 = self.curr_generation[1]
            if x == 0:
                result = line1[0:2]
                result.append(line0[1])
            elif x == self.cols - 1:
                result = line1[-2:]
                result.append(line0[x - 1])
            else:
                result = line1[x - 1:x + 2]
                result.append(line0[x - 1])
                result.append(line0[x + 1])
        elif y == self.rows - 1:
            line0 = self.curr_generation[y]
            line1 = self.curr_generation[y - 1]
            if x == 0:
                result = line1[0:2]
                result.append(line0[1])
            elif x == self.cols - 1:
                result = line1[-2:]
                result.append(line0[x - 1])
            else:
                result = line1[x - 1:x + 2]
                result.append(line0[x - 1])
                result.append(line0[x + 1])
        else:
            line0 = self.curr_generation[y]
            line1 = self.curr_generation[y - 1]
            line2 = self.curr_generation[y + 1]
            if x == 0:
                result = line1[0:2] + line2[0:2]
                result.append(line0[1])
            elif x == self.cols - 1:
                result = line1[-2:] + line2[-2:]
                result.append(line0[x - 1])
            else:
                result = line1[x - 1:x + 2] + line2[x - 1:x + 2]
                result.append(line0[x - 1])
                result.append(line0[x + 1])

        return result

    def get_neighbours(self, cell: Cell) -> Cells:
        (xx, yy) = cell
        if xx > self.rows or yy > self.cols:
            return []

        result = []
        if xx == 0:
            line0 = self.curr_generation[0]
            line1 = self.curr_generation[1]
            if yy == 0:
                result = line1[0:2]
                result.append(line0[1])
            elif yy == self.cols - 1:
                result = line1[-2:]
                result.append(line0[yy - 1])
            else:
                result = line1[yy - 1:yy + 2]
                result.append(line0[yy - 1])
                result.append(line0[yy + 1])
        elif xx == self.rows - 1:
            line0 = self.curr_generation[xx]
            line1 = self.curr_generation[xx - 1]
            if yy == 0:
                result = line1[0:2]
                result.append(line0[1])
            elif yy == self.cols - 1:
                result = line1[-2:]
                result.append(line0[yy - 1])
            else:
                result = line1[yy - 1:yy + 2]
                result.append(line0[yy - 1])
                result.append(line0[yy + 1])
        else:
            line0 = self.curr_generation[xx]
            line1 = self.curr_generation[xx - 1]
            line2 = self.curr_generation[xx + 1]
            if yy == 0:
                result = line1[0:2] + line2[0:2]
                result.append(line0[1])
            elif yy == self.cols - 1:
                result = line1[-2:] + line2[-2:]
                result.append(line0[yy - 1])
            else:
                result = line1[yy - 1:yy + 2] + line2[yy - 1:yy + 2]
                result.append(line0[yy - 1])
                result.append(line0[yy + 1])

        return result

    def get_next_generation(self) -> Grid:
        newGrid = []
        y = 0
        for line in self.curr_generation:
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

        return newGrid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        # self.draw_lines()
        # self.draw_grid()
        # pygame.display.flip()
        # clock.tick(self.speed)

        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1
        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.max_generations >= self.generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        newGrid = []
        with open(filename) as f:
            line = f.readline()[:-1]
            while line:
                newGrid.append([int(c) for c in list(line)])
                line = f.readline()[:-1]
        f.close()
        game = GameOfLife((len(newGrid), len(newGrid[0])))
        game.curr_generation = newGrid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        myOutput = ""
        for line in self.curr_generation:
            newLine = ''.join([str(i) for i in line]) + '\n'
            myOutput += newLine

        f = open(filename, "w")
        f.writelines(myOutput)
        f.close()
        pass


if __name__ == '__main__':
    # game = GameOfLife.from_file('glider.txt')
    game = GameOfLife((6, 8), max_generations=18)
    game.curr_generation = [
        [1, 1, 0, 0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1],
    ]
    for i in range(7):
        game.step()
        if i + 1 in [1, 3, 5, 7]:
            print(game.curr_generation)
