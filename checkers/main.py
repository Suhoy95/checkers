import field


class Player():
    """Класс, описывающий игрока"""
    def __init__(self, place, color, is_computer=False):
        self.place = place
        self.color = color
        self.is_computer = is_computer


class GameState():
    """Класс, описывающий игровое состояние"""
    def __init__(self, first_player, second_player):
        self.field = field.Field()
        self.first_player = first_player
        self.second_player = second_player
        self.cur_player = first_player
        self.steps = []

    def push_step(self, step):
        """Добавляет новый ход в стек ходов и выполняет его"""
        pass

    def pop_step(self):
        """Удаляет последний совершенный ход из стека и отменяет его"""
        pass

    def change_player(self):
        """Меняет текущего игрока"""
        pass

    def is_gameover(self):
        """Проверяет, закончена ли игра"""
        pass

if __name__ == '__main__':
    pass
