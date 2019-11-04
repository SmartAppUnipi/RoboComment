import unittest
from src.CommentMatcher import CommentMatcher

def test_pick_comment1():
    commentmatcher = CommentMatcher()

    jsonobj = {}
    comment = commentmatcher.pick_comment(jsonobj)

    print(comment)