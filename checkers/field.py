"""Модуль с реализацией шашечного поля"""


import enum
from collections import namedtuple


class Colors(enum.Enum):
    WHITE = 1
    BLACK = 2


Check = namedtuple('Check', ['color', 'is_queen'])
white_check = Check(Colors.WHITE, False)
black_check = Check(Colors.BLACK, False)
white_queen = Check(Colors.WHITE, True)
black_queen = Check(Colors.BLACK, True)


class Field():
    """Шашечное поле"""
    def __init__(self):
        """Создание поля со стартовой позицией"""
        self._checks = dict()
        self._lighting_cells = dict()
        self._generate_start_pos()

    def _check_coords(self, coords):
        """Проверка координат на принадлежность полю"""
        if len(coords) != 2:
            return False

        return all(map(lambda c: c > 0 and c < 11, coords))

    def _generate_start_pos(self, bottom_color=Colors.WHITE, top_color=Colors.BLACK):
        """Генерация стартовой позиции"""
        for i in range(1, 5):
            for j in range(1 + (i & 1), 11, 2):
                self._checks[(j, i)] = black_check

        for i in range(7, 11):
            for j in range(1 + (i & 1), 11, 2):                
                self._checks[(j, i)] = white_check

    def get_check(self, coords):
        """Возвращает шашку, которая стоит на соответствующей координатам клетке поля, -1, если шашки нет"""
        if not self._check_coords(coords):
            raise ValueError('coords')

        if coords not in self._checks:
            return -1

        return self._checks[coords]

    def get_checks_of_this_color(self, color):
        """Возвращает все шашки заданного цвета"""
        if color != Colors.BLACK and color != Colors.WHITE:
            raise ValueError('color')

        return filter(lambda c: c.color == color, self._checks.values())

    def move_check(self, old_coords, new_coords):
        """Передвигает шашку с координатами old_coords в клетку поля, соответствующую координатам new_coords"""
        if old_coords not in self._checks:
            raise ValueError('old_coords')

        if new_coords in self._checks:
            raise ValueError('new_coords')

        check = self._checks[old_coords]
        del self._checks[old_coords]
        self._checks[new_coords]= check

    def del_check(self, coords):
        """Удаляет шашку, которая стоит на соответствующей координатам клетке поля"""
        if coords not in self._checks:
            raise ValueError('coords')

        del self._checks[coords]

    def add_check(self, coords, check):
        """Ставит в соответствие координатам шашку"""
        if coords in self._checks:
            raise ValueError('coords')

        if not isinstance(check, Check):
            raise TypeError('check')

        self._checks[coords] = check

    def highlight_cell(self, coords):
        """Подсвечивает клетку поля, соответствующую координатам"""
        if not self._check_coords(coords):
            raise ValueError('coords')

        self._lighting_cells[coords] = True

    def is_lighting(self, coords):
        """Проверяет, подсвечена ли клетка, соответствующая координатам"""
        return coords in self._lighting_cells

    def unhighlight_cell(self, coords):
        """Убирает Подсветку с клетки поля, соответствующую координатам"""
        if coords not in self._lighting_cells:
            raise ValueError('coords')

        del self._lighting_cells[coords]

    def __str__(self):
        pass
