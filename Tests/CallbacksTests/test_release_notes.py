import unittest
from unittest.mock import patch, mock_open
from dash.exceptions import PreventUpdate
from Callbacks.ReleaseNotesPage.LoadReleaseNotes import LoadReleaseNotes
from Tests.CallbacksTests.CallbacksBaseTests import CallbacksBaseTests


class TestLoadReleaseNotes(CallbacksBaseTests):
    def setUp(self) -> None:
        super().setUp()
        self.load_release_notes = LoadReleaseNotes(self.dependency_mock)

    @patch(
        'builtins.open',
        new_callable=mock_open,
        read_data='## Version 1.0 - 2023-01-01\nContent for version 1.0\n## Version 2.0 - 2023-02-01\nContent for version 2.0\n',
    )
    def test_callback_valid_url(self, mock_file: unittest.mock.MagicMock) -> None:
        url = '/release-notes'
        style = {'justifyContent': 'center', 'text-align': 'left'}

        result = self.load_release_notes.callback(url, style)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[1], dict)
        self.assertNotIn('justifyContent', result[1])
        self.assertNotIn('text-align', result[1])

    def test_callback_invalid_url(self) -> None:
        url = '/invalid-url'
        style = {'justifyContent': 'center', 'text-align': 'left'}

        with self.assertRaises(PreventUpdate):
            self.load_release_notes.callback(url, style)
