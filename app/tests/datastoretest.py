"""Datastore unit tests."""

import sys
import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

sys.path.insert(1, 'google-cloud-sdk/platform/google_appengine')
sys.path.insert(1, 'google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.insert(1, '../lib')
sys.path.insert(1, '../')


class TestModel(ndb.Model):
    """A model class for testing."""
    number = ndb.IntegerProperty(default=42)
    text = ndb.StringProperty()


class TestEntityGroupRoot(ndb.Model):
    """Entity group root"""
    pass


class DatastoreTestCase(unittest.TestCase):
    """Class for datastore tests"""

    def setup(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        ndb.get_context().clear_cache()


        
