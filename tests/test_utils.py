import unittest

from esnbot import utils

class TestUtils(unittest.TestCase):

    def test_mention_user(self):
        correct_mention = "<@username>"

        self.assertEqual(utils.mention_user("username"), correct_mention)

# TODO add more tests