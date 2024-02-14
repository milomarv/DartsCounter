from Models.Game import Game

class State:
    def __init__(self, value):
        self.value = value

class DependencyContainer:
    def __init__(self, app):
        self.app = app
        self.game = Game()
        self.online_mode = State(False)