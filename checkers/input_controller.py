"""Модуль с функциями, позволяющими обрабатывать ввод пользователя"""


from field import field
# некруто, ничего не должно зависеть от main
# Возможно для логики стоит выделить файл GameLogic or core
# А в main только оставить точку входа + возможно, процедуру сборки существующих классов
from main import Player

# Глобально! код возврата -1 не тру (только если это не СИстемное  пограмирование)
# может None будет адекватнее

def read_check(field, player):
    """Считывает координаты клетки с шашкой, -1 в случае неудачи"""
    if not isinstance(field, Field):
        raise TypeError('field')

    if not isinstance(player, Player):
        raise TypeError('player')

    coords = None
    #some stuff
    check = field.get_check(coords)
    if check == -1 or check.color != player.color:
        return -1
    return coords


def read_cell(field, steps):
    """Считывает координаты поля для одного из возможных ходов, -1 в случае неудачи"""
    if not isinstance(field, Field):
        raise TypeError('field')

    if not isinstance(steps, list):
        raise TypeError('steps')

    if len(steps) == 0:
        return -1

    cell = None
    #some stuff
    cells_for_steps = map(lambda s: s.end_cell, steps)
    if cell not in set(cells_for_steps):
        return -1
    return cell
