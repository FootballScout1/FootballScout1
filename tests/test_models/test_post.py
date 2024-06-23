#!/usr/bin/python3
"""
Contains the TestPostDocs and TestPost classes
"""

from datetime import datetime
import inspect
import models
from models.post import Post
from models.base_model import BaseModel
import pep8
import unittest


class TestPostDocs(unittest.TestCase):
    """Tests to check the documentation and style of Post class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.post_f = inspect.getmembers(Post, inspect.isfunction)

    def test_pep8_conformance_post(self):
        """Test that models/post.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/post.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_post(self):
        """Test tests/test_models/test_post.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_post.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_post_module_docstring(self):
        """Test for the post.py module docstring"""
        self.assertIsNot(Post.__doc__, None,
                         "post.py needs a docstring")
        self.assertTrue(len(Post.__doc__) >= 1,
                        "post.py needs a docstring")

    def test_post_class_docstring(self):
        """Test for the Post class docstring"""
        self.assertIsNot(Post.__doc__, None,
                         "Post class needs a docstring")
        self.assertTrue(len(Post.__doc__) >= 1,
                        "Post class needs a docstring")

    def test_post_func_docstrings(self):
        """Test for the presence of docstrings in Post methods"""
        for func in self.post_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestPost(unittest.TestCase):
    """Test the Post class"""

    def setUp(self):
        """Set up test methods"""
        self.post = Post(
            user_id="1234",
            title="Test Title",
            content="Test Content")

    def tearDown(self):
        """Tear down test methods"""
        del self.post

    def test_is_subclass(self):
        """Test that Post is a subclass of BaseModel"""
        self.assertIsInstance(self.post, BaseModel)

    def test_user_id_attr(self):
        """Test that Post has attribute user_id and it's a string"""
        self.assertTrue(hasattr(self.post, "user_id"))
        self.assertEqual(type(self.post.user_id), str)

    def test_title_attr(self):
        """Test that Post has attribute title and it's a string"""
        self.assertTrue(hasattr(self.post, "title"))
        self.assertEqual(type(self.post.title), str)

    def test_content_attr(self):
        """Test that Post has attribute content and it's a string"""
        self.assertTrue(hasattr(self.post, "content"))
        self.assertEqual(type(self.post.content), str)

    def test_to_dict_creates_dict(self):
        """Test to_dict() creates a dictionary with proper attrs"""
        post_dict = self.post.to_dict()
        self.assertEqual(post_dict["__class__"], "Post")
        self.assertIsInstance(post_dict["created_at"], str)
        self.assertIsInstance(post_dict["updated_at"], str)

    def test_str_method(self):
        """Test the __str__ method"""
        string = "[Post] ({}) {}".format(self.post.id, self.post.__dict__)
        self.assertEqual(str(self.post), string)

    def test_save(self):
        """Test that save() updates the updated_at attribute"""
        old_updated_at = self.post.updated_at
        self.post.save()
        self.assertNotEqual(old_updated_at, self.post.updated_at)


if __name__ == "__main__":
    unittest.main()
