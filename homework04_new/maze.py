from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """
    rowLenth = len(grid[0])
    x = coord[0] - 1
    y = coord[1] + 1
    num = choice((0, 1))
    if num == 1 and x != 0 and y != rowLenth - 1 or x == 0 and y != rowLenth - 1:
        grid[x + 1][y] = " "
    elif num == 0 and x != 0 and y != rowLenth - 1 or x != 0 and y == rowLenth - 1:
        grid[x][y - 1] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for i, cell in enumerate(empty_cells):
        remove_wall(grid, cell)

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """
    return [(x, y) for x, row in enumerate(grid) for y, _ in enumerate(row) if grid[x][y] == "X"]


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            value = k + 1
            if grid[i][j] == k and grid[i][j] == 1:
                if i == 0:
                    grid[i + 1][j] = value
                if i == len(grid) - 1:
                    grid[i - 1][j] = value
                if j == 0:
                    grid[i][j + 1] = value
                if j == len(grid[0]) - 1:
                    grid[i][j - 1] = value
            elif grid[i][j] == k:
                if grid[i - 1][j] == 0:
                    grid[i - 1][j] = value
                if grid[i + 1][j] == 0:
                    grid[i + 1][j] = value
                if grid[i][j - 1] == 0:
                    grid[i][j - 1] = value
                if grid[i][j + 1] == 0:
                    grid[i][j + 1] = value
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    :param grid:
    :param exit_coord:
    :return:
    """
    result = [(exit_coord[0], exit_coord[1])]
    i = exit_coord[0]
    j = exit_coord[1]
    k = grid[i][j]
    if j - 1 >= 0 and j + 1 <= len(grid[0]) - 1:
        if grid[i][j - 1] == 1:
            result.append((i, j - 1))
            return result
        if grid[i][j + 1] == 1:
            result.append((i, j + 1))
            return result

    if i - 1 >= 0 and i + 1 <= len(grid) - 1:
        if grid[i - 1][j] == 1:
            result.append((i - 1, j))
            return result
        if grid[i + 1][j] == 1:
            result.append((i + 1, j))
            return result

    while k != 1:
        if grid[i][j] == k:
            if grid[i - 1][j] == k - 1:
                i, j = i - 1, j
            elif grid[i + 1][j] == k - 1:
                i, j = i + 1, j
            elif grid[i][j - 1] == k - 1:
                i, j = i, j - 1
            elif grid[i][j + 1] == k - 1:
                i, j = i, j + 1

            k -= 1
            result.append((i, j))

    return result


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """
    rowLenth = len(grid)
    colLenth = len(grid[0])
    if (
        coord[0] == rowLenth - 1
        and coord[1] == colLenth - 1
        or coord[0] == 0
        and coord[1] == 0
        or coord[0] == rowLenth - 1
        and coord[1] == 0
        or coord[0] == 0
        and coord[1] == colLenth - 1
    ):
        return True

    if coord[0] == 1 and coord[1] == 0 or coord[0] == 0 and coord[1] == 1:
        if grid[2][1] != " " and grid[1][2] != " " and grid[1][1] != " ":
            return True

    if coord[0] == 0 and coord[1] == colLenth - 2 or coord[0] == 1 and coord[1] == colLenth - 1:
        if (
            grid[1][colLenth - 3] != " "
            and grid[2][colLenth - 2] != " "
            and grid[1][colLenth - 2] != " "
        ):
            return True

    if coord[0] == rowLenth - 1 and coord[1] == 1 or coord[0] == rowLenth - 2 and coord[1] == 0:
        if (
            grid[rowLenth - 3][1] != " "
            and grid[rowLenth - 2][2] != " "
            and grid[rowLenth - 2][1] != " "
        ):
            return True

    if (
        coord[0] == rowLenth - 1
        and coord[1] == colLenth - 2
        or coord[0] == rowLenth - 2
        and coord[1] == colLenth - 1
    ):
        if (
            grid[rowLenth - 1][colLenth - 3] != " "
            and grid[rowLenth - 3][colLenth - 2] != " "
            and grid[rowLenth - 2][colLenth - 2] != " "
        ):
            return True

    if coord[0] == 0 and grid[1][coord[1]] != " ":
        return True

    if coord[0] == rowLenth - 1 and grid[rowLenth - 2][coord[1]] != " ":
        return True

    if coord[1] == 0 and grid[coord[0]][1] != " ":
        return True

    if coord[1] == colLenth - 1 and grid[coord[0]][colLenth - 2] != " ":
        return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    :param grid:
    :return:
    """
    rowLenth = len(grid)
    colLenth = len(grid[0])
    coord = get_exits(grid)
    if len(coord) == 1:
        return (grid, coord[0])
    if not encircled_exit(grid, coord[0]) and not encircled_exit(grid, coord[1]):
        for x in range(rowLenth):
            for y in range(colLenth):
                if grid[x][y] == " ":
                    grid[x][y] = 0
        grid[coord[0][0]][coord[0][1]] = 1
        grid[coord[1][0]][coord[1][1]] = 0
        k = 1
        while grid[coord[1][0]][coord[1][1]] == 0:
            grid = make_step(grid, k)
            k += 1
        path = shortest_path(grid, coord[1])
        for x in range(rowLenth):
            for y in range(colLenth):
                if grid[x][y] != " " and grid[x][y] != "■":
                    grid[x][y] = " "
        return grid, path
    return grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param path:
    :return:
    """
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
