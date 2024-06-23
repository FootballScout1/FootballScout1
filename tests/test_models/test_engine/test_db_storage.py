#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.club import Club
from models.location import Location
from models.player import Player
from models.scout import Scout
from models.skill import Skill
from models.rating import Rating
from models.comment import Comment
from models.like import Like
from models.post import Post
from models.user import User
import json
import os
import pep8
import unittest
from models import storage
DBStorage = db_storage.DBStorage
classes = {"Club": Club, "Location": Location, "Player": Player, "Scout": Scout, 
           "Skill": Skill, "Rating": Rating, "Comment": Comment, "Like": Like, 
           "Post": Post, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_engine/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        all_objs = models.storage.all()
        self.assertIs(type(all_objs), dict)
        self.assertGreaterEqual(len(all_objs), 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        initial_count = models.storage.count(User)
        new_user = User(email="test@test.com", password="password")
        models.storage.new(new_user)
        models.storage.save()
        new_count = models.storage.count(User)
        self.assertEqual(initial_count + 1, new_count)
        models.storage.delete(new_user)
        models.storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        new_user = User(email="test2@test.com", password="password")
        models.storage.new(new_user)
        models.storage.save()
        saved_user = models.storage.get(User, new_user.id)
        self.assertIsNotNone(saved_user)
        models.storage.delete(saved_user)
        models.storage.save()

    def test_get_db(self):
        """Tests method for obtaining an instance from db storage"""
        dic = {"name": "Test Club"}
        instance = Club(**dic)
        storage.new(instance)
        storage.save()
        get_instance = storage.get(Club, instance.id)
        self.assertEqual(get_instance, instance)
        storage.delete(instance)
        storage.save()

    def test_count(self):
        """Tests count method for db storage"""
        initial_count = storage.count(Club)
        new_club = Club(name="Test Club")
        storage.new(new_club)
        storage.save()
        self.assertEqual(storage.count(Club), initial_count + 1)
        storage.delete(new_club)
        storage.save()
        self.assertEqual(storage.count(Club), initial_count)

