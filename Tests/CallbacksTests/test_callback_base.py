from unittest.mock import Mock

from dash.exceptions import PreventUpdate
from parameterized import parameterized

from Callbacks.CallbackBase import CallbackBase
from CallbacksTests.CallbacksBaseTests import CallbacksBaseTests


class CallbacksTest(CallbacksBaseTests):
    # noinspection PyPep8Naming
    def setUp(self) -> None:
        super().setUp()

        self.dash_mock = Mock()

    @parameterized.expand([
        [[{'prop_id': 'start-stop-game-button.n_clicks', 'value': 1}], 'start-stop-game-button'],
        [[{'prop_id': '{"index":"1711716794.866656","type":"game-entry-delete-button"}.n_clicks', 'value': 1}],
         {'index': '1711716794.866656', 'type': 'game-entry-delete-button'}]
    ])
    def test_get_prop_from_context(self, triggered_prop: list[dict], desired_prop: str | dict) -> None:
        # Arrange
        self.dash_mock.callback_context.triggered = triggered_prop
        callback_base = CallbackBase(self.dependency_mock, self.dash_mock)

        # Act
        prop_id = callback_base.get_prop_from_context()

        # Assert
        self.assertEqual(desired_prop, prop_id)

    def test_get_prop_from_context_with_block_initial(self) -> None:
        # Arrange
        self.dash_mock.callback_context.triggered = None
        callback_base = CallbackBase(self.dependency_mock, self.dash_mock)

        # Act & Assert
        with self.assertRaises(PreventUpdate):
            callback_base.get_prop_from_context()

    def test_get_prop_from_context_without_block_initial(self) -> None:
        # Arrange
        self.dash_mock.callback_context.triggered = None
        callback_base = CallbackBase(self.dependency_mock, self.dash_mock)

        # Act 
        prop_id = callback_base.get_prop_from_context(block_initial = False)

        # Assert
        self.assertIsNone(prop_id)
