#!/usr/bin/python3
"""
Contains the TestUserDocs and TestUser classes
"""

from datetime import datetime
import inspect
import models
from models.user import User
from models.base_model import BaseModel
import pep8
import unittest


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of User class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.user_f = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """Test that models/user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(self):
        """Test tests/test_models/test_user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_user_module_docstring(self):
        """Test for the user.py module docstring"""
        self.assertIsNot(User.__doc__, None,
                         "user.py needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1,
                        "user.py needs a docstring")

    def test_user_class_docstring(self):
        """Test for the User class docstring"""
        self.assertIsNot(User.__doc__, None,
                         "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1,
                        "User class needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.user_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestUser(unittest.TestCase):
    """Test the User class"""
    def setUp(self):
        """Set up test methods"""
        self.user = User(email="test@example.com", password="password123", first_name="John", last_name="Doe")

    def tearDown(self):
        """Tear down test methods"""
        del self.user

    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel"""
        self.assertIsInstance(self.user, BaseModel)

    def test_email_attr(self):
        """Test that User has attribute email and it's a string"""
        self.assertTrue(hasattr(self.user, "email"))
        self.assertEqual(type(self.user.email), str)

    def test_password_attr(self):
        """Test that User has attribute password and it's a string"""
        self.assertTrue(hasattr(self.user, "password"))
        self.assertEqual(type(self.user.password), str)

    def test_first_name_attr(self):
        """Test that User has attribute first_name and it's a string"""
        self.assertTrue(hasattr(self.user, "first_name"))
        self.assertEqual(type(self.user.first_name), str)

    def test_last_name_attr(self):
        """Test that User has attribute last_name and it's a string"""
        self.assertTrue(hasattr(self.user, "last_name"))
        self.assertEqual(type(self.user.last_name), str)

    def test_to_dict_creates_dict(self):
        """Test to_dict() creates a dictionary with proper attrs"""
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict["__class__"], "User")
        self.assertIsInstance(user_dict["created_at"], str)
        self.assertIsInstance(user_dict["updated_at"], str)

    def test_str_method(self):
        """Test the __str__ method"""
        string = "[User] ({}) {}".format(self.user.id, self.user.__dict__)
        self.assertEqual(str(self.user), string)

    def test_save(self):
        """Test that save() updates the updated_at attribute"""
        old_updated_at = self.user.updated_at
        self.user.save()
        self.assertNotEqual(old_updated_at, self.user.updated_at)

    def test_password_encryption(self):
        """Test that password is encrypted with md5"""
        self.assertNotEqual(self.user.password, "password123")
        self.assertEqual(len(self.user.password), 32)  # MD5 hash length


if __name__ == "__main__":
    unittest.main()

