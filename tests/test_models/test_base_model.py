#!/usr/bin/python3
"""
Contains the TestBaseModelDocs and TestBaseModel classes
"""

from datetime import datetime
import inspect
import models
from models.base_model import BaseModel
import pep8
import unittest
import os
from time import sleep


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.base_f = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance_base_model(self):
        """Test that models/base_model.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_base_model(self):
        """Test tests/test_models/test_base_model.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_base_model_module_docstring(self):
        """Test for the base_model.py module docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "base_model.py needs a docstring")

    def test_base_model_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_base_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def setUp(self):
        """Set up test methods"""
        self.base = BaseModel()

    def tearDown(self):
        """Tear down test methods"""
        del self.base

    def test_id_is_unique(self):
        """Test that IDs are unique"""
        base2 = BaseModel()
        self.assertNotEqual(self.base.id, base2.id)

    def test_created_at_is_datetime(self):
        """Test that created_at is a datetime object"""
        self.assertIsInstance(self.base.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """Test that updated_at is a datetime object"""
        self.assertIsInstance(self.base.updated_at, datetime)

    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at attribute"""
        old_updated_at = self.base.updated_at
        sleep(1)
        self.base.save()
        self.assertNotEqual(old_updated_at, self.base.updated_at)

    def test_to_dict_creates_dict(self):
        """Test to_dict() creates a dictionary with proper attrs"""
        base_dict = self.base.to_dict()
        self.assertEqual(base_dict["__class__"], "BaseModel")
        self.assertIsInstance(base_dict["created_at"], str)
        self.assertIsInstance(base_dict["updated_at"], str)

    def test_str_method(self):
        """Test the __str__ method"""
        string = "[BaseModel] ({}) {}".format(self.base.id, self.base.__dict__)
        self.assertEqual(str(self.base), string)

    def test_kwargs_instantiation(self):
        """Test instantiation with kwargs"""
        kwargs = self.base.to_dict()
        new_base = BaseModel(**kwargs)
        self.assertEqual(self.base.id, new_base.id)
        self.assertEqual(self.base.created_at, new_base.created_at)
        self.assertEqual(self.base.updated_at, new_base.updated_at)
        self.assertNotEqual(self.base, new_base)


if __name__ == "__main__":
    unittest.main()
