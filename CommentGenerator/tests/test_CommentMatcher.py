import unittest
from src.CommentMatcher import CommentMatcher


class TestCommentMatcher(unittest.TestCase):
    def setUp(self):
        self.comment_matcher = CommentMatcher()

    def test_pick_comment1(self):
        jsonobj = {}
        comment = self.comment_matcher.pick_comment(jsonobj)

        print(comment)