#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestFootballScoutCommand_help
    TestFootballScoutCommand_exit
    TestFootballScoutCommand_create
    TestFootballScoutCommand_show
    TestFootballScoutCommand_all
    TestFootballScoutCommand_destroy
    TestFootballScoutCommand_update
"""
import os
import pycodestyle
import console
import json
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import FootballScoutCommand
from io import StringIO
from unittest.mock import patch
import models
from models.base_model import BaseModel
from models.comment import Comment
from models.like import Like
from models.player import Player
from models.rating import Rating
from models.skill import Skill
from models.club import Club
from models.location import Location
from models.post import Post
from models.scout import Scout
from models.user import User


class TestFootballScoutCommand_help(unittest.TestCase):
    """Unittests for testing help messages of
    the FootballScout command interpreter."""

    def test_help_quit(self):
        h = "Quit command to exit the program"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("help quit"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_create(self):
        h = "Create instance specified by user"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("help create"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_EOF(self):
        # h = "EOF signal to exit the program"
        h = "Exits console"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("help EOF"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_show(self):
        h = "Print string repr of a class instance, given id"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("help show"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_destroy(self):
        h = ("Delete a class instance of a given id, save result to json file")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("help destroy"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_all(self):
        h = ("Prints all string representation of all\n"
             "        instances based or not on the class name")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("help all"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_count(self):
        h = "Display count of instances specified"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("help count"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_update(self):
        h = ("Updates an instance based on the class name and id by adding or\n"
             "        updating attribute (save the change into the JSON file)")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("help update"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help(self):
        h = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("help"))
            self.assertEqual(h, output.getvalue().strip())


class TestFootballScoutCommand_exit(unittest.TestCase):
    """Unittests for testing exiting from \
            the FootballScout command interpreter."""

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(FootballScoutCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(FootballScoutCommand().onecmd("EOF"))


class TestFootballScoutCommand_create(unittest.TestCase):
    """Unittests for testing create from the \
            FootballScout command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("create"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("create MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_syntax(self):
        correct = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("MyModel.create()"))
            self.assertEqual(correct, output.getvalue().strip())
        correct = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(
                FootballScoutCommand().onecmd("BaseModel.create()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_object(self):
        models = [
            'Club',
            'Comment',
            'Like',
            'Location',
            'Player',
            'Post',
            'Rating',
            'Scout',
            'Skill',
            'User']
        for model in models:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"create {model}"))
                self.assertLess(0, len(output.getvalue().strip()))
                testKey = f"{model}.{output.getvalue().strip()}"
                self.assertIn(testKey, storage.all().keys())


class TestFootballScoutCommand_show(unittest.TestCase):
    """Unittests for testing show from the FootballScout command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_show_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("show"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd(".show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_show_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("show MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("MyModel.show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_id_space_notation(self):
        correct = "** instance id missing **"
        models = [
            'Club',
            'Comment',
            'Like',
            'Location',
            'Player',
            'Post',
            'Rating',
            'Scout',
            'Skill',
            'User']
        for model in models:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"show {model}"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_id_dot_notation(self):
        correct = "** instance id missing **"
        models = [
            'Club',
            'Comment',
            'Like',
            'Location',
            'Player',
            'Post',
            'Rating',
            'Scout',
            'Skill',
            'User']
        for model in models:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"{model}.show()"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_no_instance_found_space_notation(self):
        correct = "** no instance found **"
        models = [
            'Club',
            'Comment',
            'Like',
            'Location',
            'Player',
            'Post',
            'Rating',
            'Scout',
            'Skill',
            'User']
        for model in models:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"show {model} 1"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_no_instance_found_dot_notation(self):
        correct = "** no instance found **"
        models = [
            'Club',
            'Comment',
            'Like',
            'Location',
            'Player',
            'Post',
            'Rating',
            'Scout',
            'Skill',
            'User']
        for model in models:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"{model}.show(1)"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_objects_space_notation(self):
        models = [
            'Club',
            'Comment',
            'Like',
            'Location',
            'Player',
            'Post',
            'Rating',
            'Scout',
            'Skill',
            'User']
        for model in models:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"create {model}"))
                testID = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()[f"{model}.{testID}"]
                command = f"show {model} {testID}"
                self.assertFalse(FootballScoutCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())

    def test_show_objects_dot_notation(self):
        models = [
            'Club',
            'Comment',
            'Like',
            'Location',
            'Player',
            'Post',
            'Rating',
            'Scout',
            'Skill',
            'User']
        for model in models:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"create {model}"))
                testID = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()[f"{model}.{testID}"]
                command = f"{model}.show({testID})"
                self.assertFalse(FootballScoutCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())


class TestFootballScoutCommandDestroy(unittest.TestCase):
    """Unittests for testing destroy from the \
            FootballScoutCommand interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except FileNotFoundError:
            pass
        storage.reload()

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmp", "file.json")
        except FileNotFoundError:
            pass
        storage.reload()

    def setUp(self):
        super().setUp()
        # Clear any existing objects in the storage
        storage.__objects = {}

    def test_destroy_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("destroy"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd(".destroy()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("destroy MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(
                FootballScoutCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_id_missing(self):
        correct = "** instance id missing **"
        classes_to_test = ["Club", "Location", "Post", "Scout", "User"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"destroy {class_name}"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_id(self):
        correct = "** no instance found **"
        classes_to_test = ["Club", "Location", "Post", "Scout", "User"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"destroy {class_name} 1"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_objects(self):
        # Example for testing destroy functionality for Club model
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("create Club"))
            test_id = output.getvalue().strip()

        # Ensure we are accessing the correct format in storage
        key = f"Club.{test_id}"
        self.assertIn(key, storage.all())
        obj = storage.all()[key]

        with patch("sys.stdout", new=StringIO()) as output:
            # obj = BaseModel().objects[f"Club.{test_id}"]
            command = f"destroy Club {test_id}"
            self.assertFalse(FootballScoutCommand().onecmd(command))
            self.assertNotIn(key, storage.all())

    def test_destroy_objects_dot_notation(self):
        models_to_test = [
            ("Club", Club),
            ("Location", Location),
            ("Post", Post),
            ("Scout", Scout),
            ("User", User)

        ]

        for class_name, model_class in models_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"create {class_name}"))
                test_id = output.getvalue().strip()

            # Ensure we are accessing the correct format in storage
            key = f"{class_name}.{test_id}"
            self.assertIn(key, storage.all())
            obj = storage.all()[key]

            with patch("sys.stdout", new=StringIO()) as output:
                # obj = model_class.objects[f"{class_name}.{test_id}"]
                command = f"{class_name}.destroy({test_id})"
                self.assertFalse(FootballScoutCommand().onecmd(command))
                self.assertNotIn(key, storage.all())


class TestFootballScoutCommandAll(unittest.TestCase):
    """Unittests for testing all of the FootballScout command interpreter."""

    @classmethod
    def setUpClass(cls):
        # Implement setup actions if needed
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        # Clear objects in your models or storage here if needed
        Club.objects = {}
        Location.objects = {}
        Post.objects = {}
        Scout.objects = {}
        User.objects = {}

    @classmethod
    def tearDownClass(cls):
        # Implement teardown actions if needed
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def setUp(self):
        # Implement per-test setup actions if needed
        pass

    def tearDown(self):
        # Implement per-test teardown actions if needed
        pass

    def test_all_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("all MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("MyModel.all()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_all_objects_space_notation(self):
        models_to_test = ["Club", "Location", "Post", "Scout", "User"]
        for model_name in models_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"create {model_name}"))

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("all Club"))
            self.assertIn("Club", output.getvalue().strip())
            self.assertNotIn("Location", output.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("all Location"))
            self.assertIn("Location", output.getvalue().strip())
            self.assertNotIn("Club", output.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("all Post"))
            self.assertIn("Post", output.getvalue().strip())
            self.assertNotIn("Scout", output.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("all Scout"))
            self.assertIn("Scout", output.getvalue().strip())
            self.assertNotIn("Post", output.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("all User"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("Club", output.getvalue().strip())

    def test_all_objects_dot_notation(self):
        models_to_test = ["Club", "Location", "Post", "Scout", "User"]
        for model_name in models_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"create {model_name}"))

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("Club.all()"))
            self.assertIn("Club", output.getvalue().strip())
            self.assertNotIn("Location", output.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("Location.all()"))
            self.assertIn("Location", output.getvalue().strip())
            self.assertNotIn("Club", output.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("Post.all()"))
            self.assertIn("Post", output.getvalue().strip())
            self.assertNotIn("Scout", output.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("Scout.all()"))
            self.assertIn("Scout", output.getvalue().strip())
            self.assertNotIn("Post", output.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("User.all()"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("Club", output.getvalue().strip())


class TestFootballScoutCommandUpdate(unittest.TestCase):
    """Unittests for testing update from the \
            FootballScout command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        # Clear objects in your models or storage here if needed
        Club.objects = {}
        Location.objects = {}
        Post.objects = {}
        Scout.objects = {}
        User.objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def setUp(self):
        # Implement per-test setup actions if needed
        pass

    def tearDown(self):
        # Implement per-test teardown actions if needed
        pass

    def test_update_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("update"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd(".update()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_update_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("update MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("MyModel.update()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_id_space_notation(self):
        models_to_test = ["Club", "Location", "Post", "Scout", "User"]
        correct = "** instance id missing **"
        for model_name in models_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"update {model_name}"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_invalid_id_space_notation(self):
        models_to_test = ["Club", "Location", "Post", "Scout", "User"]
        correct = "** no instance found **"
        for model_name in models_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"update {model_name} 1"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_name_space_notation(self):
        models_to_test = ["Club", "Location", "Post", "Scout", "User"]
        correct = "** attribute name missing **"
        for model_name in models_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"create {model_name}"))
                test_id = output.getvalue().strip()
                test_cmd = f"update {model_name} {test_id}"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(FootballScoutCommand().onecmd(test_cmd))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_value_space_notation(self):
        models_to_test = ["Club", "Location", "Post", "Scout", "User"]
        correct = "** value missing **"
        for model_name in models_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                FootballScoutCommand().onecmd(f"create {model_name}")
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                test_cmd = f"update {model_name} {test_id} attr_name"
                self.assertFalse(FootballScoutCommand().onecmd(test_cmd))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_valid_string_attr_space_notation(self):
        models_to_test = ["Club", "Location", "Post", "Scout", "User"]
        for model_name in models_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"create {model_name}"))
                # FootballScoutCommand().onecmd(f"create {model_name}")
                test_id = output.getvalue().strip()

            test_cmd = f"update {model_name} {test_id} attr_name 'attr_value'"
            self.assertFalse(FootballScoutCommand().onecmd(test_cmd))

            # Access the updated object directly from storage and check
            # attribute
            try:
                obj = models.storage.all()[f"{model_name}.{test_id}"]
                self.assertEqual(getattr(obj, 'attr_name', None), "attr_value")
            except KeyError:
                self.fail(
                    f"Object with ID {test_id} not \
                            found in {model_name} storage")
            #    obj = eval(f"{model_name}.objects['{test_id}']")
            #    self.assertEqual(obj.attr_name, "attr_value")
            # except KeyError:
            #    self.fail(f"Object with ID {test_id} \
            #        not found in {model_name} storage")

            # test_dict = eval(f"{model_name}.objects['{test_id}'].__dict__")
            # self.assertEqual("attr_value", test_dict["attr_name"])


class TestFootballScoutCommandCount(unittest.TestCase):
    """Unittests for testing count method of \
            FootballScout command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        # Clear objects in your models or storage here if needed
        Club.objects = {}
        Location.objects = {}
        Post.objects = {}
        Scout.objects = {}
        User.objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def setUp(self):
        # Implement per-test setup actions if needed
        pass

    def tearDown(self):
        # Implement per-test teardown actions if needed
        pass

    def test_count_invalid_class(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(FootballScoutCommand().onecmd("MyModel.count()"))
            """self.assertEqual("0", output.getvalue().strip())"""

    def test_count_object(self):
        models_to_test = ["Club", "Location", "Post", "Scout", "User"]
        for model_name in models_to_test:
            storage.all().clear()
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"create {model_name}"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    FootballScoutCommand().onecmd(f"{model_name}.count()"))
                self.assertEqual("1", output.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
