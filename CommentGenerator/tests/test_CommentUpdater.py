import unittest
from src.CommentUpdater import CommentUpdater

def test_update_comment1():
    cu = CommentUpdater()

    updated_comment = cu.update_comment("Cristiano Ronaldo has made a goal")
    print(updated_comment)

