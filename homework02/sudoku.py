import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """
    Прочитать Судоку из указанного файла
    """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """
    Вывод Судоку
    """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    result = []
    # if len(values) != 81:
    for i in range(0, len(values), n):
        result.append(values[i : i + n])
    return result


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    result: tp.List[str] = []
    for row in grid:
        result.append(row[pos[1]])
    return result


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    firstRow = (pos[0] // 3) * 3
    firstCol = (pos[1] // 3) * 3

    result: tp.List[str] = []
    for row in range(firstRow, firstRow + 3):
        for col in range(firstCol, firstCol + 3):
            result.append(grid[row][col])
    return result


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == ".":
                return row, col
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    possibleValues = {s for s in list("123456789")}
    possibleValues = possibleValues.difference(get_row(grid, pos))
    possibleValues = possibleValues.difference(get_col(grid, pos))
    possibleValues = possibleValues.difference(get_block(grid, pos))
    return possibleValues


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """
    Решение пазла, заданного в grid

    Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if pos is None:
        return grid

    for value in find_possible_values(grid, pos):
        grid[pos[0]][pos[1]] = value
        result = solve(grid)
        if result is not None:
            return result
    grid[pos[0]][pos[1]] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """
    Если решение solution верно, то вернуть True, в противном случае False
    """
    # TODO: Add doctests with bad puzzles
    possibleValues = {s for s in list("123456789")}

    # Checking rows
    col = 0
    for row in range(len(solution)):
        pos = row, col
        testRow = get_row(solution, pos)
        if (len(possibleValues.intersection(set(testRow))) != 9) or find_empty_positions(
            solution
        ) is not None:
            return False

    # Checking cols
    row = 0
    for col in range(len(solution)):
        pos = row, col
        testCol = get_col(solution, pos)
        if (len(possibleValues.intersection(set(testCol))) != 9) or find_empty_positions(
            solution
        ) is not None:
            return False

    # Checking blocks
    for row in range(0, len(solution), 3):
        for col in range(0, len(solution), 3):
            pos = row, col
            testBlock = get_block(solution, pos)
            if (len(possibleValues.intersection(set(testBlock))) != 9) or find_empty_positions(
                solution
            ) is not None:
                return False

    return True


def randomize(arr: tp.List[tp.List[str]]):
    row = random.randint(0, 8)
    col = random.randint(0, 8)
    if arr[row][col] != ".":
        arr[row][col] = "."
        return arr
    else:
        result = randomize(arr)
        return result


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """
    Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    default_data = [["." for _ in range(9)] for _ in range(9)]
    if N == 0:
        return default_data

    result = solve(default_data)
    if result is None:
        return default_data

    resultSolved: tp.List[tp.List[str]] = result
    for step in range(81 - N):
        resultSolved = randomize(resultSolved)
    return resultSolved


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
