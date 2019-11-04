import unittest
from src.CommentUpdater import CommentUpdater


class TestCommentUpdater(unittest.TestCase):

    def setUp(self):
        self.comment_updater = CommentUpdater()

    def test_update_comment1(self):

        updated_comment = self.comment_updater.update_comment("Cristiano Ronaldo has made a goal")
        print(updated_comment)

