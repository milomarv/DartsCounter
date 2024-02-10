from Models.Game import Game

class DependencyContainer:
    def __init__(self, app):
        self.app = app
        self.game = Game()