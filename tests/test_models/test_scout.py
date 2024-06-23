#!/usr/bin/python3
"""
Contains the TestScoutDocs and TestScout classes
"""

from datetime import datetime
import inspect
import models
from models.scout import Scout
from models.base_model import BaseModel
import pep8
import unittest


class TestScoutDocs(unittest.TestCase):
    """Tests to check the documentation and style of Scout class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.scout_f = inspect.getmembers(Scout, inspect.isfunction)

    def test_pep8_conformance_scout(self):
        """Test that models/scout.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/scout.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_scout(self):
        """Test tests/test_models/test_scout.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_scout.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_scout_module_docstring(self):
        """Test for the scout.py module docstring"""
        self.assertIsNot(Scout.__doc__, None,
                         "scout.py needs a docstring")
        self.assertTrue(len(Scout.__doc__) >= 1,
                        "scout.py needs a docstring")

    def test_scout_class_docstring(self):
        """Test for the Scout class docstring"""
        self.assertIsNot(Scout.__doc__, None,
                         "Scout class needs a docstring")
        self.assertTrue(len(Scout.__doc__) >= 1,
                        "Scout class needs a docstring")

    def test_scout_func_docstrings(self):
        """Test for the presence of docstrings in Scout methods"""
        for func in self.scout_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestScout(unittest.TestCase):
    """Test the Scout class"""
    def setUp(self):
        """Set up test methods"""
        self.scout = Scout(email="test@example.com", password="password123", first_name="John", last_name="Doe")

    def tearDown(self):
        """Tear down test methods"""
        del self.scout

    def test_is_subclass(self):
        """Test that Scout is a subclass of BaseModel"""
        self.assertIsInstance(self.scout, BaseModel)

    def test_email_attr(self):
        """Test that Scout has attribute email and it's a string"""
        self.assertTrue(hasattr(self.scout, "email"))
        self.assertEqual(type(self.scout.email), str)

    def test_password_attr(self):
        """Test that Scout has attribute password and it's a string"""
        self.assertTrue(hasattr(self.scout, "password"))
        self.assertEqual(type(self.scout.password), str)

    def test_first_name_attr(self):
        """Test that Scout has attribute first_name and it's a string"""
        self.assertTrue(hasattr(self.scout, "first_name"))
        self.assertEqual(type(self.scout.first_name), str)

    def test_last_name_attr(self):
        """Test that Scout has attribute last_name and it's a string"""
        self.assertTrue(hasattr(self.scout, "last_name"))
        self.assertEqual(type(self.scout.last_name), str)

    def test_to_dict_creates_dict(self):
        """Test to_dict() creates a dictionary with proper attrs"""
        scout_dict = self.scout.to_dict()
        self.assertEqual(scout_dict["__class__"], "Scout")
        self.assertIsInstance(scout_dict["created_at"], str)
        self.assertIsInstance(scout_dict["updated_at"], str)

    def test_str_method(self):
        """Test the __str__ method"""
        string = "[Scout] ({}) {}".format(self.scout.id, self.scout.__dict__)
        self.assertEqual(str(self.scout), string)

    def test_save(self):
        """Test that save() updates the updated_at attribute"""
        old_updated_at = self.scout.updated_at
        self.scout.save()
        self.assertNotEqual(old_updated_at, self.scout.updated_at)

    def test_password_encryption(self):
        """Test that password is encrypted with md5"""
        self.assertNotEqual(self.scout.password, "password123")
        self.assertEqual(len(self.scout.password), 32)  # MD5 hash length


if __name__ == "__main__":
    unittest.main()

