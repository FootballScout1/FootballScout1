#!/usr/bin/python3
"""
Contains the TestFileStorageDocs and TestFileStorage classes
"""

from datetime import datetime
import inspect
import models
from models.base_model import BaseModel
from models.engine import file_storage
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
FileStorage = file_storage.FileStorage
classes = {"Club": Club, "BaseModel": BaseModel, "Location": Location,
           "Player": Player, "Scout": Scout, "Skill": Skill,
           "Rating": Rating, "Comment": Comment, "Like": Like,
           "Post": Post, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_engine/test_file_storage.py \
                conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_models/test_engine/test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def setUp(self):
        """Set up test methods"""
        self.storage = FileStorage()
        self.storage.reload()

    def tearDown(self):
        """Tear down test methods"""
        del self.storage

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(self.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        all_objs = self.storage.all()
        self.assertIs(type(all_objs), dict)
        self.assertGreaterEqual(len(all_objs), 0)

    def test_new(self):
        """Test that new adds an object to the file storage"""
        initial_count = len(self.storage.all(User))
        new_user = User(email="test@test.com", password="password")
        self.storage.new(new_user)
        self.storage.save()
        new_count = len(self.storage.all(User))
        self.assertEqual(initial_count + 1, new_count)

    def test_save(self):
        """Test that save properly saves objects to file.json"""
        new_user = User(email="test2@test.com", password="password")
        self.storage.new(new_user)
        self.storage.save()
        with open("file.json", "r") as f:
            data = json.load(f)
        key = "User." + new_user.id
        self.assertIn(key, data)

    def test_reload(self):
        """Test that reload properly loads objects from file.json"""
        new_user = User(email="test3@test.com", password="password")
        self.storage.new(new_user)
        self.storage.save()
        self.storage.reload()
        reloaded_user = self.storage.get(User, new_user.id)
        self.assertIsNotNone(reloaded_user)
        self.assertEqual(new_user.email, reloaded_user.email)

    def test_delete(self):
        """Test that delete removes an object from file storage"""
        new_user = User(email="test4@test.com", password="password")
        self.storage.new(new_user)
        self.storage.save()
        self.storage.delete(new_user)
        self.storage.save()
        self.assertIsNone(self.storage.get(User, new_user.id))

    def test_get(self):
        """Tests method for obtaining an instance file storage"""
        new_user = User(email="test5@test.com", password="password")
        self.storage.new(new_user)
        self.storage.save()
        get_instance = self.storage.get(User, new_user.id)
        self.assertEqual(get_instance, new_user)

    def test_count(self):
        """Tests count method for file storage"""
        initial_count = self.storage.count(User)
        new_user = User(email="test6@test.com", password="password")
        self.storage.new(new_user)
        self.storage.save()
        self.assertEqual(self.storage.count(User), initial_count + 1)
        self.storage.delete(new_user)
        self.storage.save()
        self.assertEqual(self.storage.count(User), initial_count)
