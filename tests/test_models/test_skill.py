#!/usr/bin/python3
"""
Contains the TestSkillDocs and TestSkill classes
"""

import inspect
import models
from models.skill import Skill
from models.base_model import BaseModel
import pep8
import unittest


class TestSkillDocs(unittest.TestCase):
    """Tests to check the documentation and style of Skill class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.skill_f = inspect.getmembers(Skill, inspect.isfunction)

    def test_pep8_conformance_skill(self):
        """Test that models/skill.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/skill.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_skill(self):
        """Test tests/test_models/test_skill.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_skill.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_skill_module_docstring(self):
        """Test for the skill.py module docstring"""
        self.assertIsNot(Skill.__doc__, None,
                         "skill.py needs a docstring")
        self.assertTrue(len(Skill.__doc__) >= 1,
                        "skill.py needs a docstring")

    def test_skill_class_docstring(self):
        """Test for the Skill class docstring"""
        self.assertIsNot(Skill.__doc__, None,
                         "Skill class needs a docstring")
        self.assertTrue(len(Skill.__doc__) >= 1,
                        "Skill class needs a docstring")

    def test_skill_func_docstrings(self):
        """Test for the presence of docstrings in Skill methods"""
        for func in self.skill_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestSkill(unittest.TestCase):
    """Test the Skill class"""
    def setUp(self):
        """Set up test methods"""
        self.skill = Skill(name="Dribbling")

    def tearDown(self):
        """Tear down test methods"""
        del self.skill

    def test_is_subclass(self):
        """Test that Skill is a subclass of BaseModel"""
        self.assertIsInstance(self.skill, BaseModel)

    def test_name_attr(self):
        """Test that Skill has attribute name and it's a string"""
        self.assertTrue(hasattr(self.skill, "name"))
        self.assertEqual(type(self.skill.name), str)

    def test_to_dict_creates_dict(self):
        """Test to_dict() creates a dictionary with proper attrs"""
        skill_dict = self.skill.to_dict()
        self.assertEqual(skill_dict["__class__"], "Skill")
        self.assertIsInstance(skill_dict["created_at"], str)
        self.assertIsInstance(skill_dict["updated_at"], str)

    def test_str_method(self):
        """Test the __str__ method"""
        string = "[Skill] ({}) {}".format(self.skill.id, self.skill.__dict__)
        self.assertEqual(str(self.skill), string)

    def test_save(self):
        """Test that save() updates the updated_at attribute"""
        old_updated_at = self.skill.updated_at
        self.skill.save()
        self.assertNotEqual(old_updated_at, self.skill.updated_at)


if __name__ == "__main__":
    unittest.main()

