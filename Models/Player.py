from Logging.Logger import Logger

class Player:
    def __init__(self, name):
        self.logger = Logger(__name__)
        self.name = name
        self.logger.info(f"Player {name} created")
    
    def __str__(self):
        return f"Player: {self.name}"