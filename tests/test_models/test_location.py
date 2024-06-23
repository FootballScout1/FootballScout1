#!/usr/bin/python3
"""
Contains the TestLocationDocs and TestLocation classes
"""

from datetime import datetime
import inspect
import models
from models.location import Location
from models.base_model import BaseModel
import pep8
import unittest


class TestLocationDocs(unittest.TestCase):
    """Tests to check the documentation and style of Location class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.location_f = inspect.getmembers(Location, inspect.isfunction)

    def test_pep8_conformance_location(self):
        """Test that models/location.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/location.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_location(self):
        """Test tests/test_models/test_location.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_location.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_location_module_docstring(self):
        """Test for the location.py module docstring"""
        self.assertIsNot(Location.__doc__, None,
                         "location.py needs a docstring")
        self.assertTrue(len(Location.__doc__) >= 1,
                        "location.py needs a docstring")

    def test_location_class_docstring(self):
        """Test for the Location class docstring"""
        self.assertIsNot(Location.__doc__, None,
                         "Location class needs a docstring")
        self.assertTrue(len(Location.__doc__) >= 1,
                        "Location class needs a docstring")

    def test_location_func_docstrings(self):
        """Test for the presence of docstrings in Location methods"""
        for func in self.location_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestLocation(unittest.TestCase):
    """Test the Location class"""
    def setUp(self):
        """Set up test methods"""
        self.location = Location(name="Jakarta")

    def tearDown(self):
        """Tear down test methods"""
        del self.location

    def test_is_subclass(self):
        """Test that Location is a subclass of BaseModel"""
        self.assertIsInstance(self.location, BaseModel)

    def test_name_attr(self):
        """Test that Location has attribute name and it's a string"""
        self.assertTrue(hasattr(self.location, "name"))
        self.assertEqual(type(self.location.name), str)

    def test_to_dict_creates_dict(self):
        """Test to_dict() creates a dictionary with proper attrs"""
        location_dict = self.location.to_dict()
        self.assertEqual(location_dict["__class__"], "Location")
        self.assertIsInstance(location_dict["created_at"], str)
        self.assertIsInstance(location_dict["updated_at"], str)

    def test_str_method(self):
        """Test the __str__ method"""
        string = "[Location] ({}) {}".format(self.location.id, self.location.__dict__)
        self.assertEqual(str(self.location), string)

    def test_save(self):
        """Test that save() updates the updated_at attribute"""
        old_updated_at = self.location.updated_at
        self.location.save()
        self.assertNotEqual(old_updated_at, self.location.updated_at)


if __name__ == "__main__":
    unittest.main()

