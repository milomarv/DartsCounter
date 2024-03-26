import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s')


class Logger:
    def __init__(self, name_space: str):
        self.nameSpace = name_space
        self.logger = logging.getLogger(self.nameSpace)

        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
