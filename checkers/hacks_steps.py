"""Модуль, отвечающий за поиск и исполнение ходов и рубок"""


from . import field


class Step():
    """
        Класс, описывающий ход
        hacked_checks[k] == ((x, y), check)
    """
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


class Node():
    """Вершина дерева рубок"""
    def __init__(self, coords):
        self.coords = coords
        self.childs = []
        self.parrent = None

    def add_child(self, num):
        """Добавляет ребенка"""
        self.childs.append(num)

    def add_parrent(self, num):
        """Добавляет родителя"""
        self.parrent = num

class HacksTree():
    """Дерево рубок"""
    def __init__(self):
        self._nodes = []

    def add(self, coords):
        """Добавляет новую вершину, присваивает ей уникальный номер и возвращает его"""
        self._nodes.append(Node(coords))
        return len(self._nodes) - 1

    def get(self, num):
        """Возвращает вершину по ее уникальному номеру"""
        if num < 0 or num >= len(self._nodes):
            raise ValueError('num')

        return self._nodes[num]

    def incident(self, num1, num2):
        """Создает ребро из вершины с номером num1 в вершину с номером num2"""
        if num1 < 0 or num1 >= len(self._nodes):
            raise ValueError('num1')

        if num2 < 0 or num2 >= len(self._nodes):
            raise ValueError('num2')

        self._nodes[num1].add_child(num2)
        self._nodes[num2].add_parrent(num1)

    def _get_ends_of_brenches(self):
        """возвращает концы веток"""
        return filter(lambda n: len(n.childs) == 0, self._nodes)

    def _get_depth_of_brench(self, node):
        """Возвращает глубину ветки"""
        depth = 0
        while node is not None:
            node = node.parrent
            depth += 1

        return depth

    def get_longest_brenches(self):
        """Возвращает самые длинные ветки"""
        brenches = ((i, self._get_depth_of_brench(i)) for i in self._get_ends_of_brenches())
        max_depth = max(brenches, key=lambda b: b[1])

        for b in brenches:
            if b[1] == max_depth:
                yield b[0]

    def is_hacked_in_branch(self, num, coords):
        """Проверяет, была ли срублена шашка с координатами coords в ветке"""
        node = self._nodes[num]
        while node.parrent is not None:
            x = abs(node.coords[0] - node.parrent.coords[0])
            y = abs(node.coords[1] - node.parrent.coords[1])
            if (x, y) == coords:
                return True
            node = node.parrent

        return False

def get_steps(check, coords):
    """Возвращает все возможные ходы шашки из заданной позиции"""
    pass
