from unittest.mock import Mock

from BaseTests import BaseTests
from Callbacks.Router.RouterConfig import RouterConfig


class CallbacksBaseTests(BaseTests):
    # noinspection PyPep8Naming
    def setUp(self) -> None:
        super().setUp()
        self.dependency_mock = Mock()
        self.dependency_mock.router_config = RouterConfig()
