"""Модуль, отвечающий за поиск и хранение ходов и рубок"""


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

    def __eq__(self, other):
        """Сравнивает два хода"""
        if not isinstance(other, Step):
            raise TypeError('other')

        return (
            set(self.hacked_checks) == set(other.hacked_checks) and
            self.start_coor == other.start_coor and
            self.end_coor == other.end_coor and
            self.is_become_queen == other.is_become_queen)


class Node():
    """Класс, описывающий вершину дерева рубок"""
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

    def __eq__(self, other):
        if not isinstance(other, Node):
            raise TypeError('other')

        return (
            self.coords == other.coords and
            set(self.childs) == set(other.childs) and
            self.parrent == other.parrent)


def get_coords_of_check(start_coords, end_coords):
    """Возвращает координаты шашки, которая была срублена ходом из start_coords в end_coords"""
    x = (start_coords[0] + end_coords[0]) / 2
    y = (start_coords[1] + end_coords[1]) / 2

    return (x, y)


class HacksTree():
    """Класс, описывающий дерево рубок"""
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
        """Возвращает глубину ветки, концом которой является node"""
        depth = 0
        while node is not None:
            node = node.parrent
            depth += 1

        return depth

    def _get_longest_brenches(self):
        """Возвращает концы самых длинных веток"""
        brenches = ((i, self._get_depth_of_brench(i)) for i in self._get_ends_of_brenches())
        max_depth = max(brenches, key=lambda b: b[1])

        for b in brenches:
            if b[1] == max_depth:
                yield b[0]

    def generate_steps(self, chess_field, place_for_becoming_queen):
        """Генерирует экземпляры класса Step на основе построенного дерева"""
        if not isinstance(chess_field, field.Field):
            raise TypeError('chess_field')

        steps = []

        for b in self._get_longest_brenches():
            is_become_queen = b.coords == place_for_becoming_queen
            end_coords = b.coords
            hacked_checks = []
            while b.parrent is not None:
                hacked_check_coords = get_coords_of_check(b.coords, b.parrent.coords)
                hacked_checks.append((hacked_check_coords, field.get_check((x, y))))
                b = b.parrent
            s = Step(b.coords, end_coords, hacked_checks, is_become_queen)
            steps.append(s)

            return steps

    def is_hacked_in_branch(self, num, coords):
        """
            Проверяет, была ли срублена шашка с координатами coords в ветке,
            концом которой является вершина с номером num
        """
        node = self._nodes[num]
        while node.parrent is not None:
            hacked_check_coords = get_coords_of_check(node.coords, node.parrent.coords)
            if hacked_check_coords == coords:
                return True
            node = node.parrent

        return False

def _get_cur_hacks(chess_field, check, coords):
    """Возвращает все рубки глубины один из заданных координат"""
    if not isinstance(check, field.Check):
        raise TypeError('check')

    if not isinstance(chess_field, field.Field):
        raise TypeError('chess_field')

    dirs = [(-1, -1), (1, -1), (1, 1), (-1, 1)]

    get_moved_point = lambda p, d: (p[0] + d[0], p[1] + d[1])

    for d in dirs:
        coords_of_cur_cell = get_moved_point(coords, d)
        cur_check = -1
        try:
            cur_check = chess_field.get_check(coords_of_cur_cell)

            while cur_check == -1:
                if not check.is_queen:
                    break
                coords_of_cur_cell = get_moved_point(coords_of_cur_cell, d)
                cur_check = chess_field.get_check(coords_of_cur_cell)
        except ValueError:
            continue

        if (
                isinstance(cur_check, field.Check) and 
                cur_check.color != check.color):
            hacked_check = cur_check

            coords_of_cur_cell = get_moved_point(coords_of_cur_cell, d)
            try:
                cur_check = chess_field.get_check(coords_of_cur_cell)

                while cur_check == -1:
                    yield coords_of_cur_cell

                    if not check.is_queen:
                        break
                    coords_of_cur_cell = get_moved_point(coords_of_cur_cell, d)
                    cur_check = chess_field.get_check(coords_of_cur_cell)
            except ValueError:
                pass

def _get_hacks(chess_field, coords, place_for_becoming_queen):
    """Возвращает все рубки максимальной глубины из заданных координат"""
    if not isinstance(chess_field, field.Field):
        raise TypeError('chess_field')

    check = chess_field.get_check(coords)

    t = HacksTree()
    hacks = []
    num_of_cur_hack = t.add(coords)
    hacks.append(num_of_cur_hack)

    #DFS
    while len(hacks) > 0:
        num_of_cur_hack = hacks.pop()
        cur_hack = t.get(num_of_cur_hack)

        for i in _get_cur_hacks(chess_field, check, cur_hack.coords):
            hacked_check_coords = get_coords_of_check(cur_hack.coords, i)

            if not t.is_hacked_in_branch(num_of_cur_hack, hacked_check_coords):
                num_of_incident_hack = t.add(i)
                t.incident(num_of_cur_hack, num_of_incident_hack)
                hacks.append(num_of_incident_hack)

    return t.generate_steps(chess_field, place_for_becoming_queen)

def get_steps(chess_field, check, coords, place_for_becoming_queen):
    """Возвращает все возможные ходы шашки из заданных координат"""
    if not isinstance(check, field.Check):
        raise TypeError('check')

    if not isinstance(chess_field, field.Field):
        raise TypeError('chess_field')

    steps = _get_hacks(check, coords, place_for_becoming_queen)

    if len(steps) == 0:
        pass

    return steps
