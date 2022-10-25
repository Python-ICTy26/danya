import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: float = float("inf"),
        grid: tp.Optional[Grid] = None,
    ) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = grid if grid else self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        return [[0] * self.cols for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell

        init_poss = (
            (row, col - 1),
            (row - 1, col),
            (row, col + 1),
            (row + 1, col),
            (row - 1, col - 1),
            (row - 1, col + 1),
            (row + 1, col - 1),
            (row + 1, col + 1),
        )

        poss = []
        for row, col in init_poss:
            if row >= 0 and col >= 0:
                try:
                    near_cell = self.curr_generation[row][col]
                    poss += [near_cell]
                except IndexError:
                    continue

        return poss

    def get_next_generation(self) -> Grid:
        new_grid = [row.copy() for row in self.curr_generation]
        for row in range(self.rows):
            for col in range(self.cols):
                neighbours = self.get_neighbours((row, col))
                alive_neighbours_count = sum(neighbours)

                value = self.curr_generation[row][col]

                if not value and alive_neighbours_count == 3:
                    new_grid[row][col] = 1
                elif value and alive_neighbours_count not in (2, 3):
                    new_grid[row][col] = 0

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation, self.curr_generation = (
            self.curr_generation,
            self.get_next_generation(),
        )
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: str) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename, "r")
        grid = []
        for i, line in enumerate(f):
            row = []
            for value in line[:-1]:
                row.append(int(value))
            grid += [row]
        return GameOfLife(size=(len(grid), len(grid[0])), grid=grid)

    def save(self, filename: str) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, "w")
        grid_str = "\n".join("".join(str(value) for value in row) for row in self.curr_generation)
        f.write(grid_str)
