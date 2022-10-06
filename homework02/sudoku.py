import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
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
    res = []
    while len(values) >= n:
        res.append([values.pop(0) for _ in range(n)])
    return res


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return [arr[pos[1]] for arr in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row, col = pos
    if not 0 <= row <= 8 or not 0 <= col <= 8 or len(grid) != 9:
        raise Exception
    return [
        grid[x][y]
        for x in range(row // 3 * 3, row // 3 * 3 + 3)
        for y in range(col // 3 * 3, col // 3 * 3 + 3)
    ]


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    for i in range(len(grid)):
        arr = grid[i]
        for j in range(len(arr)):
            ch = arr[j]
            if ch == ".":
                return (i, j)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    block = get_block(grid, pos)
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    return set("123456789") - set(block) - set(row) - set(col)


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    empty = find_empty_positions(grid)
    if not empty:
        return grid
    values = find_possible_values(grid, empty)
    newGrid = [list(arr) for arr in grid]
    for value in values:
        newGrid[empty[0]][empty[1]] = value
        res = solve(newGrid)
        if res:
            return res
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    full = set("123456789")
    for i in range(len(solution)):
        for j in range(len(solution)):
            if (
                set(get_block(solution, (i, j))) != full
                or set(get_row(solution, (i, j))) != full
                or set(get_col(solution, (i, j))) != full
            ):
                return False
    return True


def generate_sudoku(N: int):
    init = solve([["."] * 9 for _ in range(9)])
    count = 0
    while count < 81 - N:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if init and init[row][col] != ".":
            init[row][col] = "."
            count += 1
    return init


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
