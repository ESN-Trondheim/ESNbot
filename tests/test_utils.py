import unittest
import os
import time

from pathlib import Path
from unittest import mock

from esnbot import utils


class TestUtils(unittest.TestCase):
    def test_mention_user(self):
        expected_mention = "<@username>"
        self.assertEqual(utils.mention_user("username"), expected_mention)

    def test_mention_bot(self):
        expected_response_none = ""
        self.assertEqual(utils.mention_bot(), expected_response_none)

        os.environ["BOT_ID"] = "bot_id"
        expected_response_value = f"<@{os.environ.get('BOT_ID')}>"
        self.assertEqual(utils.mention_bot(), expected_response_value)

    @mock.patch("time.localtime", mock.Mock(return_value=(2023, 1, 1, 0, 0, 0, 0, 1, 0)))
    def test_timestamp(self):
        expected_time = time.strftime("%d-%m-%Y %H:%M:%S: ", time.localtime())
        self.assertEqual(utils.timestamp(), expected_time)

    @mock.patch("builtins.print")
    @mock.patch("time.localtime", mock.Mock(return_value=(2023, 1, 1, 0, 0, 0, 0, 1, 0)))
    def test_log_to_console(self, mock_print):
        timestamp = utils.timestamp()
        text = "Foo bar baz"
        expected_function_call = [mock.call(f"{timestamp}{text}", flush=True)]
        utils.log_to_console(text)
        self.assertEqual(mock_print.mock_calls, expected_function_call)

    @mock.patch("time.localtime", mock.Mock(return_value=(2023, 1, 1, 0, 0, 0, 0, 1, 0)))
    def test_log_to_file(self):
        filename = "test_log_to_file.txt"
        message = "Foo"
        expected_file_content = "01-01-2023 00:00:00: Foo\n"

        utils.log_to_file(filename, message, "w")

        with open(filename, "r") as file:
            result_file_content = file.read()

        self.assertTrue(
            os.path.isfile(Path.cwd().joinpath(filename))
        )  # Maybe not necessary, tested indirectly through the opening of the file above
        self.assertEqual(result_file_content, expected_file_content)
        Path.cwd().joinpath(filename).unlink()

    # This test is not really necessary right now, as the function just calls two other functions.
    # However if log_to_file_anc_console() is modified, the test is ready.
    @mock.patch("builtins.print")
    @mock.patch("time.localtime", mock.Mock(return_value=(2023, 1, 1, 0, 0, 0, 0, 1, 0)))
    def test_log_to_file_and_console(self, mock_print):
        timestamp = utils.timestamp()
        filename = "test_log_to_file_and_console.txt"
        message = "Foo"
        expected_file_content = "01-01-2023 00:00:00: Foo\n"
        expected_function_call = [mock.call(f"{timestamp}{message}", flush=True)]

        utils.log_to_file_and_console(filename, message, "w")

        with open(filename, "r") as file:
            result_file_content = file.read()

        self.assertEqual(mock_print.mock_calls, expected_function_call)
        self.assertTrue(
            os.path.isfile(Path.cwd().joinpath(filename))
        )  # Maybe not necessary here either
        self.assertEqual(result_file_content, expected_file_content)
        Path.cwd().joinpath(filename).unlink()
