#!/usr/bin/python3
"""
Contains the TestCommentDocs and TestComment classes
"""

from datetime import datetime
import inspect
import models
from models.comment import Comment
from models.base_model import BaseModel
import pep8
import unittest


class TestCommentDocs(unittest.TestCase):
    """Tests to check the documentation and style of Comment class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.comment_f = inspect.getmembers(Comment, inspect.isfunction)

    def test_pep8_conformance_comment(self):
        """Test that models/comment.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/comment.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_comment(self):
        """Test tests/test_models/test_comment.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_comment.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_comment_module_docstring(self):
        """Test for the comment.py module docstring"""
        self.assertIsNot(Comment.__doc__, None,
                         "comment.py needs a docstring")
        self.assertTrue(len(Comment.__doc__) >= 1,
                        "comment.py needs a docstring")

    def test_comment_class_docstring(self):
        """Test for the Comment class docstring"""
        self.assertIsNot(Comment.__doc__, None,
                         "Comment class needs a docstring")
        self.assertTrue(len(Comment.__doc__) >= 1,
                        "Comment class needs a docstring")

    def test_comment_func_docstrings(self):
        """Test for the presence of docstrings in Comment methods"""
        for func in self.comment_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestComment(unittest.TestCase):
    """Test the Comment class"""

    def setUp(self):
        """Set up test methods"""
        self.comment = Comment(
            post_id="1234",
            user_id="5678",
            text="Nice post!")

    def tearDown(self):
        """Tear down test methods"""
        del self.comment

    def test_is_subclass(self):
        """Test that Comment is a subclass of BaseModel"""
        self.assertIsInstance(self.comment, BaseModel)

    def test_post_id_attr(self):
        """Test that Comment has attribute post_id and it's a string"""
        self.assertTrue(hasattr(self.comment, "post_id"))
        self.assertEqual(type(self.comment.post_id), str)

    def test_user_id_attr(self):
        """Test that Comment has attribute user_id and it's a string"""
        self.assertTrue(hasattr(self.comment, "user_id"))
        self.assertEqual(type(self.comment.user_id), str)

    def test_text_attr(self):
        """Test that Comment has attribute text and it's a string"""
        self.assertTrue(hasattr(self.comment, "text"))
        self.assertEqual(type(self.comment.text), str)

    def test_to_dict_creates_dict(self):
        """Test to_dict() creates a dictionary with proper attrs"""
        comment_dict = self.comment.to_dict()
        self.assertEqual(comment_dict["__class__"], "Comment")
        self.assertIsInstance(comment_dict["created_at"], str)
        self.assertIsInstance(comment_dict["updated_at"], str)

    def test_str_method(self):
        """Test the __str__ method"""
        string = "[Comment] ({}) {}".format(
            self.comment.id, self.comment.__dict__)
        self.assertEqual(str(self.comment), string)

    def test_save(self):
        """Test that save() updates the updated_at attribute"""
        old_updated_at = self.comment.updated_at
        self.comment.save()
        self.assertNotEqual(old_updated_at, self.comment.updated_at)


if __name__ == "__main__":
    unittest.main()
