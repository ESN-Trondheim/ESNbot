import unittest
from unittest import mock
import os
import time

# To be able to run just this module standalone from tests directory
import sys
sys.path.append("..")

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

    @mock.patch("time.localtime", mock.Mock(return_value = (2023, 1, 1, 0, 0, 0, 0, 1, 0)))
    def test_timestamp(self):
        expected_time = time.strftime("%d-%m-%Y %H:%M:%S: ", time.localtime())
        self.assertEqual(utils.timestamp(), expected_time)

    # @mock.patch("builtins.print")
    # @mock.patch("time.localtime", mock.Mock(return_value = (2023, 1, 1, 0, 0, 0, 0, 1, 0)))
    # def test_log_to_console(self, mock_print):
    #     time_print = utils.timestamp()
    #     utils.log_to_console("Lorem ipsum")
    #     assert mock_print.assert_called_with(f"{time_print}Lorem ipsum", flush=True)

    def test_log_to_file(self):
        pass

    def test_log_to_file_and_console(self):
        pass


# TODO add more tests
if __name__ == "__main__":
    unittest.main()
