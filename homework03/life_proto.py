import random
import typing as tp

import pygame
from pygame import QUIT
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()
            self.draw_lines()

            self.grid = self.get_next_generation()

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
            return [
                [random.randint(0, 1) for _ in range(self.cell_width)]
                for _ in range(self.cell_height)
            ]
        return [[0] * self.cell_width for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                value = self.grid[row][col]
                color = pygame.Color("green") if value else pygame.Color("white")
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size
                    ),
                )
        return None

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
                    near_cell = self.grid[row][col]
                    poss += [near_cell]
                except IndexError:
                    continue
        return poss

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = [row.copy() for row in self.grid]
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                neighbours = self.get_neighbours((row, col))
                alive_neighbours_count = sum(neighbours)

                if not self.grid[row][col] and alive_neighbours_count == 3:
                    new_grid[row][col] = 1
                elif self.grid[row][col] and alive_neighbours_count not in (2, 3):
                    new_grid[row][col] = 0

        return new_grid


if __name__ == "__main__":
    game = GameOfLife(500, 500, 30, 10)
    game.run()
