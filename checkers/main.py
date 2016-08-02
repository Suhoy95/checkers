import field


class Player():
    """Класс, описывающий игрока"""
    # Если place - визуальное положение игрока на доске, то насколько оно важно в задаче?
    # В принципе, цвет может определять положение.  
    def __init__(self, place, color, is_computer=False):
        self.place = place
        self.color = color
        self.is_computer = is_computer


class GameState():
    """Класс, описывающий игровое состояние"""
    def __init__(self, first_player, second_player):
        self.chess_field = field.Field()
        self.first_player = first_player
        self.second_player = second_player
        self.cur_player = first_player # current_player, сокращения могут мешать
        self.steps = []

    # Внимание, Overengineering!
    # пока конструктор потянет, в будующем можно сделать так:
    # так ты сможешь создовать игровое состояние более гибко
    def __init__(self, first_player, second_player, field = field.Field(), steps = []):
        self.field = field
        self.first_player = first_player
        self.second_player = second_player
        self.cur_player = first_player
        self.steps = steps

    # Внимание, Overengineering! 
    # будет прикольно, если эти методы будут возвращать self
    # тогда можно будет вызывать их в цепочке
    # state.push_step()
    #      .change_player()
    def push_step(self, step):
        """Добавляет новый ход в стек ходов и выполняет его"""
        steps.append(step)
        self.chess_field.do_step(step)

    def pop_step(self):
        """Удаляет последний совершенный ход из стека и отменяет его"""
        step = steps.pop()
        self.chess_field.undo_step(step)

    def change_player(self):
        """Меняет текущего игрока"""
        pass

    def is_gameover(self):
        """Проверяет, закончена ли игра"""
        pass

if __name__ == '__main__':
    pass
