import unittest
from src.Filler import Filler


class TestFiller(unittest.TestCase):

    def setUp(self):
        self.comment_filler = Filler()

    def test_update_comment1(self):

        updated_comment = self.comment_filler.update_comment("Cristiano Ronaldo has made a goal")
        print(updated_comment)

