#!/usr/bin/python3
"""
Contains the TestClubDocs and TestClub classes
"""

from datetime import datetime
import inspect
import models
from models.club import Club
from models.base_model import BaseModel
from models.location import Location
import pep8
import unittest


class TestClubDocs(unittest.TestCase):
    """Tests to check the documentation and style of Club class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.club_f = inspect.getmembers(Club, inspect.isfunction)

    def test_pep8_conformance_club(self):
        """Test that models/club.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/club.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_club(self):
        """Test tests/test_models/test_club.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_club.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_club_module_docstring(self):
        """Test for the club.py module docstring"""
        self.assertIsNot(Club.__doc__, None,
                         "club.py needs a docstring")
        self.assertTrue(len(Club.__doc__) >= 1,
                        "club.py needs a docstring")

    def test_club_class_docstring(self):
        """Test for the Club class docstring"""
        self.assertIsNot(Club.__doc__, None,
                         "Club class needs a docstring")
        self.assertTrue(len(Club.__doc__) >= 1,
                        "Club class needs a docstring")

    def test_club_func_docstrings(self):
        """Test for the presence of docstrings in Club methods"""
        for func in self.club_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestClub(unittest.TestCase):
    """Test the Club class"""
    def setUp(self):
        """Set up test methods"""
        self.club = Club(name="Test Club", location_id="1234")

    def tearDown(self):
        """Tear down test methods"""
        del self.club

    def test_is_subclass(self):
        """Test that Club is a subclass of BaseModel"""
        self.assertIsInstance(self.club, BaseModel)

    def test_name_attr(self):
        """Test that Club has attribute name and it's a string"""
        self.assertTrue(hasattr(self.club, "name"))
        self.assertEqual(type(self.club.name), str)

    def test_location_id_attr(self):
        """Test that Club has attribute location_id and it's a string"""
        self.assertTrue(hasattr(self.club, "location_id"))
        self.assertEqual(type(self.club.location_id), str)

    def test_to_dict_creates_dict(self):
        """Test to_dict() creates a dictionary with proper attrs"""
        club_dict = self.club.to_dict()
        self.assertEqual(club_dict["__class__"], "Club")
        self.assertIsInstance(club_dict["created_at"], str)
        self.assertIsInstance(club_dict["updated_at"], str)

    def test_str_method(self):
        """Test the __str__ method"""
        string = "[Club] ({}) {}".format(self.club.id, self.club.__dict__)
        self.assertEqual(str(self.club), string)

    def test_save(self):
        """Test that save() updates the updated_at attribute"""
        old_updated_at = self.club.updated_at
        self.club.save()
        self.assertNotEqual(old_updated_at, self.club.updated_at)


if __name__ == "__main__":
    unittest.main()

