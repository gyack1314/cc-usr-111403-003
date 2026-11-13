"""已有接口的核心、边界及错误路径。"""
import unittest,tempfile
from pathlib import Path
from lake.storage import read_source,Objects,digest

class StorageTests(unittest.TestCase):
    def test_source_and_corruption(self):
        value=read_source()
        with tempfile.TemporaryDirectory() as d:
            o=Objects(d);key=o.put(value);self.assertEqual(o.get(key),value)
            self.assertEqual(o.put(value),key)
            Path(d,key).write_bytes(b'bad')
            with self.assertRaises(ValueError):o.get(key)
    def test_bad_object_identity(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):Objects(d).get('../bad')

from lake.asof import candidate,preference
from lake.streams import OnceRows

class FeatureTests(unittest.TestCase):
    def test_direction_and_tie(self):
        l={'product':'P','source':'S','t':10};a=dict(l,t=8,priority=1,row_id='a');b=dict(a,priority=2,row_id='b')
        self.assertTrue(candidate(l,a,'backward',2));self.assertFalse(candidate(l,a,'forward',2))
        self.assertLess(preference(l,b,'nearest'),preference(l,a,'nearest'))
        self.assertFalse(candidate(l,dict(a,t=10),'nearest',2,False))
    def test_null_and_invalid(self):
        l={'product':None,'source':'S','t':10}
        self.assertFalse(candidate(l,dict(l,priority=0,row_id='r'),'backward',2))
        with self.assertRaises(ValueError):candidate(l,l,'backward',-1)
    def test_once_stream(self):
        s=OnceRows([{'x':1}]);self.assertEqual(len(list(s)),1);self.assertTrue(s.closed)
        with self.assertRaises(RuntimeError):list(s)
