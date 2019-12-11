import unittest
from src.CommentatorPool import SymbolicEventsCache
import json
import os
import shutil



class TestSymbolicEventsCache(unittest.TestCase):
    def setUp(self):
        self.cache = SymbolicEventsCache()
    
    def symolic_json_path(self, matchid, clipid, start_time, end_time):
        clipid = hash(clipid)
        return self.cache.cache_path + "/" +  str(matchid) + "/" + str(clipid) + "/" + str(start_time) + "_" + str(end_time) + ".json"

    def tearDown(self):
        shutil.rmtree(self.cache.cache_path)
        return

    def test_get_clip_path(self):
        match_id = 42
        clip_uri = "http://match.clip/juve/inter"

        assert self.cache._get_clip_path(match_id, clip_uri) == self.cache._get_clip_path(match_id, clip_uri)


    def test_cache_event1(self):
        match_id = 42
        clip_uri = "http://match.clip/juve/inter"

        in_cache = self.cache.in_cache(match_id,clip_uri)
        assert in_cache == False

        self.cache.cache_event(match_id,clip_uri, { "start_time" : 1, "end_time" : 2})

        in_cache = self.cache.in_cache(match_id,clip_uri)
        assert in_cache == True
    

    def test_get_events1(self):
        match_id = 42
        clip_uri = "http://match.clip/juve/inter"

        self.cache.cache_event(match_id,clip_uri, { "start_time" : 1, "end_time" : 4})
        self.cache.cache_event(match_id,clip_uri, { "start_time" : 1, "end_time" : 5})
        self.cache.cache_event(match_id,clip_uri, { "start_time" : 2, "end_time" : 5})

        events = self.cache.get_events(match_id,clip_uri)

        assert events[0]['start_time'] == 1 and events[0]['end_time'] == 4
        assert events[1]['start_time'] == 1 and events[1]['end_time'] == 5
        assert events[2]['start_time'] == 2 and events[2]['end_time'] == 5
        


