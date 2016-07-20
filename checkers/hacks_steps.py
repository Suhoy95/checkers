"""Модуль, отвечающий за поиск и исполнение ходов и рубок"""


from . import field


class Step():
    """Класс, описывающий ход"""
    def __init__(
            self, start_coor, end_coor,
            hacked_checks=[], is_become_queen=False):
        if not field.Field.check_coords(start_coor):
            raise ValueError('start_coor')

        if not field.Field.check_coords(end_coor):
            raise ValueError('end_coor')

        self.start_coor = start_coor
        self.end_coor = end_coor
        self.hacked_checks = hacked_checks
        self.is_become_queen = is_become_queen

    def do(self, chess_field):
        """Исполняет ход над полем"""
        if not isinstance(chess_field, field.Field):
            raise TypeError('field')

        chess_field.move_check(self.start_coor, self.end_coor)
        if self.is_become_queen:
            chess_field.update_check(end_coor)
        for c in map(lambda a: a[0], self.hacked_checks):
            chess_field.del_check(c)

    def undo(self, field):
        """Отменяет ход над полем"""
        if not isinstance(field, field.Field):
            raise TypeError('field')

        field.move_check(end_coor, start_coor)
        if self.is_become_queen:
            field.update_check(start_coor)
        for c in self.hacked_checks:
            field.add_check(*c)

    def __eq__(self, other):
        """Сравнивает два хода"""
        if not isinstance(other, Step):
            raise TypeError('other')

        return (
            len(self.hacked_checks) == len(other.hacked_checks) and
            all(map(lambda a: a[0] == a[1], zip(self.hacked_checks, other.hacked_checks))) and
            self.start_coor == other.start_coor and
            self.end_coor == other.end_coor and
            self.is_become_queen == other.is_become_queen)
