#!/usr/bin/python3
"""
Contains the TestRatingDocs and TestRating classes
"""

from datetime import datetime
import inspect
import models
from models.rating import Rating
from models.base_model import BaseModel
import pep8
import unittest


class TestRatingDocs(unittest.TestCase):
    """Tests to check the documentation and style of Rating class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.rating_f = inspect.getmembers(Rating, inspect.isfunction)

    def test_pep8_conformance_rating(self):
        """Test that models/rating.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/rating.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_rating(self):
        """Test tests/test_models/test_rating.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_rating.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_rating_module_docstring(self):
        """Test for the rating.py module docstring"""
        self.assertIsNot(Rating.__doc__, None,
                         "rating.py needs a docstring")
        self.assertTrue(len(Rating.__doc__) >= 1,
                        "rating.py needs a docstring")

    def test_rating_class_docstring(self):
        """Test for the Rating class docstring"""
        self.assertIsNot(Rating.__doc__, None,
                         "Rating class needs a docstring")
        self.assertTrue(len(Rating.__doc__) >= 1,
                        "Rating class needs a docstring")

    def test_rating_func_docstrings(self):
        """Test for the presence of docstrings in Rating methods"""
        for func in self.rating_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestRating(unittest.TestCase):
    """Test the Rating class"""
    def setUp(self):
        """Set up test methods"""
        self.rating = Rating(player_id="1234", scout_id="5678", score=8, comment="Good player")

    def tearDown(self):
        """Tear down test methods"""
        del self.rating

    def test_is_subclass(self):
        """Test that Rating is a subclass of BaseModel"""
        self.assertIsInstance(self.rating, BaseModel)

    def test_player_id_attr(self):
        """Test that Rating has attribute player_id and it's a string"""
        self.assertTrue(hasattr(self.rating, "player_id"))
        self.assertEqual(type(self.rating.player_id), str)

    def test_scout_id_attr(self):
        """Test that Rating has attribute scout_id and it's a string"""
        self.assertTrue(hasattr(self.rating, "scout_id"))
        self.assertEqual(type(self.rating.scout_id), str)

    def test_score_attr(self):
        """Test that Rating has attribute score and it's an int"""
        self.assertTrue(hasattr(self.rating, "score"))
        self.assertEqual(type(self.rating.score), int)

    def test_comment_attr(self):
        """Test that Rating has attribute comment and it's a string"""
        self.assertTrue(hasattr(self.rating, "comment"))
        self.assertEqual(type(self.rating.comment), str)

    def test_to_dict_creates_dict(self):
        """Test to_dict() creates a dictionary with proper attrs"""
        rating_dict = self.rating.to_dict()
        self.assertEqual(rating_dict["__class__"], "Rating")
        self.assertIsInstance(rating_dict["created_at"], str)
        self.assertIsInstance(rating_dict["updated_at"], str)

    def test_str_method(self):
        """Test the __str__ method"""
        string = "[Rating] ({}) {}".format(self.rating.id, self.rating.__dict__)
        self.assertEqual(str(self.rating), string)

    def test_save(self):
        """Test that save() updates the updated_at attribute"""
        old_updated_at = self.rating.updated_at
        self.rating.save()
        self.assertNotEqual(old_updated_at, self.rating.updated_at)


if __name__ == "__main__":
    unittest.main()

