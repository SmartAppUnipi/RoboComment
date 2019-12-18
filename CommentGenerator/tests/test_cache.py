import unittest
from src.CommentatorPool import SymbolicEventsCache
import json
import os
import shutil



class TestSymbolicEventsCache(unittest.TestCase):
    def setUp(self):
        self.cache = SymbolicEventsCache()

    def tearDown(self):
        shutil.rmtree(self.cache.cache_path)
        return

    def test_in_cache(self):
        match_id = 42
        clip_uri = "http://match.clip/juve/inter"

        in_cache = self.cache.in_cache(match_id,clip_uri)
        assert in_cache == False

        self.cache.cache_event(match_id,clip_uri, { "type" : "action","start_time" : 1, "end_time" : 2})

        in_cache = self.cache.in_cache(match_id,clip_uri)
        assert in_cache == True
    

    def test_get_action1(self):
        match_id = 42
        clip_uri = "http://match.clip/juve/inter"

        self.cache.cache_event(match_id,clip_uri, { "type" : "action", "start_time" : 1, "end_time" : 4})
        self.cache.cache_event(match_id,clip_uri, { "type" : "action", "start_time" : 1, "end_time" : 5})
        self.cache.cache_event(match_id,clip_uri, { "type" : "action", "start_time" : 2, "end_time" : 5})

        events = [e for e in self.cache.get_next_event(match_id,clip_uri)]

        assert events[0]['start_time'] == 1 and events[0]['end_time'] == 4
        assert events[1]['start_time'] == 1 and events[1]['end_time'] == 5
        assert events[2]['start_time'] == 2 and events[2]['end_time'] == 5
    
    def test_cache_position1(self):
        match_id = 42
        clip_uri = "http://match.clip/juve/inter"

        self.cache.cache_event(match_id,clip_uri, { "type" : "positions", "positionX" : 1, "positionY" : 4})
        self.cache.cache_event(match_id,clip_uri, { "type" : "action", "start_time" : 1, "end_time" : 5})
        self.cache.cache_event(match_id,clip_uri, { "type" : "positions", "positionX" : 5, "positionY" : 1})

        events = [e for e in self.cache.get_next_event(match_id,clip_uri)]

        assert events[0]["positionX"] == 1 and events[0]["positionY"] == 4
        assert events[1]['start_time'] == 1 and events[1]['end_time'] == 5
        assert events[2]["positionX" ] == 5 and events[2]["positionY"] == 1

        


