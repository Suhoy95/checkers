"""Модуль с реализацией шашечного поля"""


import enum
from collections import namedtuple, OrderedDict
from . import hacks_steps


class Colors(enum.Enum):
    WHITE = 1
    BLACK = 2


Check = namedtuple('Check', ['color', 'is_queen'])
white_check = Check(Colors.WHITE, False)
black_check = Check(Colors.BLACK, False)
white_queen = Check(Colors.WHITE, True)
black_queen = Check(Colors.BLACK, True)


class Field():
    """Класс, описывающий шашечное поле"""
    def __init__(self, bottom_check=white_check, top_check=black_check, empty=False):
        """Создает поле со стартовой позицией"""
        self._checks = OrderedDict()

        if not empty:
            self._checks = Field.generate_start_pos(bottom_check, top_check)

    @staticmethod
    def check_coords(coords):
        """Проверка координат на принадлежность полю"""
        if len(coords) != 2:
            return False

        return all(map(lambda c: c > 0 and c < 11, coords))

    @staticmethod
    def generate_start_pos(bottom_check, top_check):
        """Генерирует стартовую позицию"""
        if not isinstance(bottom_check, Check):
            raise TypeError('bottom_check')

        if not isinstance(bottom_check, Check):
            raise TypeError('bottom_check')

        checks = OrderedDict()

        for i in range(1, 5):
            for j in range(1 + (i & 1), 11, 2):
                checks[(j, i)] = top_check

        for i in range(7, 11):
            for j in range(1 + (i & 1), 11, 2):                
                checks[(j, i)] = bottom_check

        return checks

    def get_check(self, coords):
        """Возвращает шашку, которая стоит на соответствующей координатам клетке поля, -1, если шашки нет"""
        if not Field.check_coords(coords):
            raise ValueError('coords')

        if coords not in self._checks:
            return -1

        return self._checks[coords]

    def get_checks_of_this_color(self, color):
        """Возвращает все шашки заданного цвета"""
        if color != Colors.BLACK and color != Colors.WHITE:
            raise ValueError('color')

        return map(lambda c: c[0], 
            filter(lambda c: c[1].color == color, self._checks.items()))

    def move_check(self, old_coords, new_coords):
        """Передвигает шашку с координатами old_coords в клетку поля, соответствующую координатам new_coords"""
        if old_coords not in self._checks:
            raise ValueError('old_coords')

        if new_coords in self._checks:
            raise ValueError('new_coords')

        check = self._checks[old_coords]
        del self._checks[old_coords]
        self._checks[new_coords]= check

    def update_check(self, coords):
        """Меняет статус шашки с дамки на обычную и обратно"""
        if coords not in self._checks:
            raise ValueError('coords')

        if not self._checks[coords].is_queen:
            self._checks[coords] = (
                white_queen if self._checks[coords] == white_check
                else black_queen
            )
        elif self._checks[coords].is_queen:
            self._checks[coords] = (
                white_check if self._checks[coords] == white_queen
                else black_check
            )

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

    def do_step(self, step):
        """Исполняет ход над полем"""
        if not isinstance(step, hacks_steps.Step):
            raise TypeError('step')

        self.move_check(step.start_coor, step.end_coor)
        if step.is_become_queen:
            self.update_check(step.end_coor)
        for c in map(lambda a: a[0], step.hacked_checks):
            self.del_check(c)

    def undo_step(self, step):
        """Отменяет ход над полем"""
        if not isinstance(step, hacks_steps.Step):
            raise TypeError('step')

        self.move_check(step.end_coor, step.start_coor)
        if step.is_become_queen:
            self.update_check(step.start_coor)
        for c in step.hacked_checks:
            self.add_check(*c)

    def __eq__(self, other):
        """Сравнивает два поля"""
        if not isinstance(other, Field):
            raise TypeError('other')

        if len(self._checks) != len(other._checks):
            return False

        for key, value in self._checks.items():
            if key not in other._checks.keys():
                return False

            if value != other._checks[key]:
                return False

        return True
