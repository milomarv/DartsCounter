from unittest.mock import Mock

from BaseTests import BaseTests


class CallbacksBaseTests(BaseTests):
    # noinspection PyPep8Naming
    def setUp(self) -> None:
        super().setUp()
        self.dependency_mock = Mock()
