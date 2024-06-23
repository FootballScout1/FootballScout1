#!/usr/bin/python3
"""
Contains the TestPlayerDocs and TestPlayer classes
"""

from datetime import datetime
import inspect
import models
from models.player import Player
from models.base_model import BaseModel
import pep8
import unittest


class TestPlayerDocs(unittest.TestCase):
    """Tests to check the documentation and style of Player class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.player_f = inspect.getmembers(Player, inspect.isfunction)

    def test_pep8_conformance_player(self):
        """Test that models/player.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/player.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_player(self):
        """Test tests/test_models/test_player.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_player.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_player_module_docstring(self):
        """Test for the player.py module docstring"""
        self.assertIsNot(Player.__doc__, None,
                         "player.py needs a docstring")
        self.assertTrue(len(Player.__doc__) >= 1,
                        "player.py needs a docstring")

    def test_player_class_docstring(self):
        """Test for the Player class docstring"""
        self.assertIsNot(Player.__doc__, None,
                         "Player class needs a docstring")
        self.assertTrue(len(Player.__doc__) >= 1,
                        "Player class needs a docstring")

    def test_player_func_docstrings(self):
        """Test for the presence of docstrings in Player methods"""
        for func in self.player_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestPlayer(unittest.TestCase):
    """Test the Player class"""
    def setUp(self):
        """Set up test methods"""
        self.player = Player(club_id="1234", name="John Doe", position="Forward", age=25, skill_level=85)

    def tearDown(self):
        """Tear down test methods"""
        del self.player

    def test_is_subclass(self):
        """Test that Player is a subclass of BaseModel"""
        self.assertIsInstance(self.player, BaseModel)

    def test_club_id_attr(self):
        """Test that Player has attribute club_id and it's a string"""
        self.assertTrue(hasattr(self.player, "club_id"))
        self.assertEqual(type(self.player.club_id), str)

    def test_name_attr(self):
        """Test that Player has attribute name and it's a string"""
        self.assertTrue(hasattr(self.player, "name"))
        self.assertEqual(type(self.player.name), str)

    def test_position_attr(self):
        """Test that Player has attribute position and it's a string"""
        self.assertTrue(hasattr(self.player, "position"))
        self.assertEqual(type(self.player.position), str)

    def test_age_attr(self):
        """Test that Player has attribute age and it's an int"""
        self.assertTrue(hasattr(self.player, "age"))
        self.assertEqual(type(self.player.age), int)

    def test_skill_level_attr(self):
        """Test that Player has attribute skill_level and it's an int"""
        self.assertTrue(hasattr(self.player, "skill_level"))
        self.assertEqual(type(self.player.skill_level), int)

    def test_to_dict_creates_dict(self):
        """Test to_dict() creates a dictionary with proper attrs"""
        player_dict = self.player.to_dict()
        self.assertEqual(player_dict["__class__"], "Player")
        self.assertIsInstance(player_dict["created_at"], str)
        self.assertIsInstance(player_dict["updated_at"], str)

    def test_str_method(self):
        """Test the __str__ method"""
        string = "[Player] ({}) {}".format(self.player.id, self.player.__dict__)
        self.assertEqual(str(self.player), string)

    def test_save(self):
        """Test that save() updates the updated_at attribute"""
        old_updated_at = self.player.updated_at
        self.player.save()
        self.assertNotEqual(old_updated_at, self.player.updated_at)


if __name__ == "__main__":
    unittest.main()

