#!/usr/bin/python3
"""
Contains the TestLikeDocs and TestLike classes
"""

from datetime import datetime
import inspect
import models
from models.like import Like
from models.base_model import BaseModel
import pep8
import unittest


class TestLikeDocs(unittest.TestCase):
    """Tests to check the documentation and style of Like class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.like_f = inspect.getmembers(Like, inspect.isfunction)

    def test_pep8_conformance_like(self):
        """Test that models/like.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/like.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_like(self):
        """Test tests/test_models/test_like.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_like.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_like_module_docstring(self):
        """Test for the like.py module docstring"""
        self.assertIsNot(Like.__doc__, None,
                         "like.py needs a docstring")
        self.assertTrue(len(Like.__doc__) >= 1,
                        "like.py needs a docstring")

    def test_like_class_docstring(self):
        """Test for the Like class docstring"""
        self.assertIsNot(Like.__doc__, None,
                         "Like class needs a docstring")
        self.assertTrue(len(Like.__doc__) >= 1,
                        "Like class needs a docstring")

    def test_like_func_docstrings(self):
        """Test for the presence of docstrings in Like methods"""
        for func in self.like_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestLike(unittest.TestCase):
    """Test the Like class"""
    def setUp(self):
        """Set up test methods"""
        self.like = Like(post_id="1234", user_id="5678")

    def tearDown(self):
        """Tear down test methods"""
        del self.like

    def test_is_subclass(self):
        """Test that Like is a subclass of BaseModel"""
        self.assertIsInstance(self.like, BaseModel)

    def test_post_id_attr(self):
        """Test that Like has attribute post_id and it's a string"""
        self.assertTrue(hasattr(self.like, "post_id"))
        self.assertEqual(type(self.like.post_id), str)

    def test_user_id_attr(self):
        """Test that Like has attribute user_id and it's a string"""
        self.assertTrue(hasattr(self.like, "user_id"))
        self.assertEqual(type(self.like.user_id), str)

    def test_to_dict_creates_dict(self):
        """Test to_dict() creates a dictionary with proper attrs"""
        like_dict = self.like.to_dict()
        self.assertEqual(like_dict["__class__"], "Like")
        self.assertIsInstance(like_dict["created_at"], str)
        self.assertIsInstance(like_dict["updated_at"], str)

    def test_str_method(self):
        """Test the __str__ method"""
        string = "[Like] ({}) {}".format(self.like.id, self.like.__dict__)
        self.assertEqual(str(self.like), string)

    def test_save(self):
        """Test that save() updates the updated_at attribute"""
        old_updated_at = self.like.updated_at
        self.like.save()
        self.assertNotEqual(old_updated_at, self.like.updated_at)


if __name__ == "__main__":
    unittest.main()

