#!/usr/bin/python3
""" console """

import cmd
import shlex  # for splitting the line along spaces except in double quotes
import re
import ast
from datetime import datetime
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

classes = {"BaseModel": BaseModel, "Comment": Comment, "Like": Like,
           "Player": Player, "Rating": Rating, "Skill": Skill,
           "Club": Club, "Location": Location,
           "Post": Post, "Scout": Scout, "User": User}


class FootballScoutCommand(cmd.Cmd):
    """ FootballScout1 console """
    prompt = '(football_scout) '
    valid_classes = classes

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """Overwriting the emptyline method"""
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_create(self, arg):
        """Create instance specified by user"""
        if not arg:
            print("** class name missing **")
            return

        if arg not in self.valid_classes:
            print("** class doesn't exist **")
            return

        new_instance = eval(f"{arg}()")
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Print string repr of a class instance, given id"""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        if args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        class_name = args[0]
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        if key not in models.storage.all():
            print("** no instance found **")
            return

        print(models.storage.all()[key])

    def do_destroy(self, arg):
        """Delete a class instance of a given id, save result to json file"""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        if args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        if key not in models.storage.all():
            print("** no instance found **")
            return

        del models.storage.all()[key]
        models.storage.save()

    def do_count(self, arg):
        """Display count of instances specified"""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        if args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return

        class_type = self.valid_classes[args[0]]
        objects = models.storage.all().values()
        count = sum(1 for obj in objects if isinstance(obj, class_type))
        print(count)

    def default(self, line):
        args = line.split('.', 1)
        if len(args) == 2:
            class_name, method_arg = args
            if method_arg == 'count()':
                self.do_count(class_name)
                return
            elif method_arg == 'create()':
                print(f"*** Unknown syntax: {class_name}.create()")
                return
            elif method_arg.startswith('show(') and method_arg.endswith(')'):
                id_str = method_arg[5:-1]
                self.do_show(f"{class_name} {id_str}")
                return
            elif method_arg == "all()":
                self.do_all(class_name)
                return
            elif method_arg.startswith('destroy(') and \
                    method_arg.endswith(')'):
                instance_id = method_arg[8:-1]
                self.do_destroy(f"{class_name} {instance_id}")
                return
            elif re.match(r"(\w+)\.(\w+)\((.*)\)", line):
                pattern_match = re.match(r"(\w+)\.(\w+)\((.*)\)", line)
                pattern = list(pattern_match.groups())
                if pattern[-1] == "":
                    pattern.pop()
                if pattern:
                    if len(pattern) >= 2:
                        class_name, method = pattern[0], pattern[1]
                        line = f"{method} {class_name}"
                        try:
                            dict = re.findall(r"\{.*?\}", pattern[2])[0]
                            if method == "update" and dict:
                                dict = eval(dict)
                                split_pattern = shlex.split(pattern[2])
                                instance_id = split_pattern[0].replace(",", "")
                                line += f" {instance_id} {dict}"
                                self.onecmd(line.strip())
                                return
                        except IndexError:
                            pass
                        if len(pattern) >= 3:
                            list_info = re.findall(r"\[.*\]", pattern[2])
                            if list_info:
                                old_val = str(list_info[0])
                                pattern[2] = pattern[2].replace(old_val, "")
                        try:
                            more_arg = shlex.split(pattern[2])
                            line += " "
                            line += " ".join(more_arg).replace(",", "")
                            line += f" {list_info or ''}"
                        except (ValueError, IndexError):
                            pass
            else:
                # print("** invalid syntax **")
                print("** class name missing **")
                return
            self.onecmd(line.strip())
            return

    def do_all(self, arg):
        """Prints all string representation of all
        instances based or not on the class name"""
        args = shlex.split(arg)
        objects = models.storage.all()
        if args:
            class_name = args[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
            else:
                for obj in objects.values():
                    if type(obj) is self.valid_classes[class_name]:
                        print(str(obj))
        else:
            print(str([str(obj) for obj in objects.values()]))

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file)"""
        if arg == "":
            print("** class name missing **")
            return
        elif re.findall(r"\{.*?\}", arg):
            pattr = r'(\w+)?\s?([\da-f-]+)?\s?({.*})?'
            match1 = re.match(pattr, arg)
            if match1:
                class_name = match1.group(1)
                instance_id = match1.group(2)
                dictionary_representation = match1.group(3)
                key = "{}.{}".format(class_name, instance_id)
                if key not in models.storage.all():
                    if class_name is None:
                        print("** class name missing **")
                        return
                    if class_name not in self.valid_classes:
                        print("** class doesn't exist **")
                        return
                    if instance_id not in models.storage.all():
                        print("** no instance found **")
                        return
                obj = models.storage.all()[key]
                dict = re.findall(r"\{.*?\}", arg)
                if dict:
                    dictionary_string = dict[0].strip("'")
                    try:
                        dict_repr = ast.literal_eval(dictionary_string)
                    except (ValueError, SyntaxError):
                        print("** invalid dictionary representation **")
                        return
                    for attr_name, attr_value in dict_repr.items():
                        setattr(obj, attr_name, attr_value)
        else:
            patt = r'(\w+)\("([\da-f-]+)"(?:, "(\w+)")?(?:, "(\w+)")?\)'
            patt2 = (r"(\w+)?\s?([\da-f-]+)?\s?(\w+)?\s?"
                     r"((\d+\.?\d*)|(\d*\.?\d+)|\"([^\"]*)\"|'([^']*)')?")
            mach = re.match(patt, arg)
            mach2 = re.match(patt2, arg)
            if mach:
                class_name = mach.group(1)
                instance_id = mach.group(2)
                attribute_name = mach.group(3)
                attribute_value = mach.group(4)
                key = "{}.{}".format(class_name, instance_id)
                if key not in models.storage.all():
                    if class_name is None:
                        print("** class name missing **")
                        return
                    if class_name not in self.valid_classes:
                        print("** class doesn't exist **")
                        return
                    if instance_id not in models.storage.all():
                        print("** no instance found **")
                        return
                elif key in models.storage.all():
                    if attribute_name is None and attribute_value is None:
                        print("** attribute name missing **")
                        return
                    elif attribute_name is not None and \
                            attribute_value is None:
                        print("** value missing **")
                        return
                attr_name = attribute_name
                attr_value = attribute_value
                obj = models.storage.all()[key]
                try:
                    attr_value = eval(attr_value)
                except (NameError, SyntaxError):
                    pass
                setattr(obj, attr_name, attr_value)
            else:
                if mach2:
                    class_name = mach2.group(1)
                    instance_id = mach2.group(2)
                    attribute_name = mach2.group(3)
                    attribute_value = mach2.group(4)
                    key = "{}.{}".format(class_name, instance_id)
                    if key not in models.storage.all():
                        if class_name is None:
                            print("** class name missing **")
                            return
                        if class_name not in self.valid_classes:
                            print("** class doesn't exist **")
                            return
                        if class_name and instance_id is None:
                            print("** instance id missing **")
                            return
                        if instance_id not in models.storage.all():
                            print("** no instance found **")
                            return
                    elif key in models.storage.all():
                        if attribute_name is None and attribute_value is None:
                            print("** attribute name missing **")
                            return
                        elif attribute_name is not None and \
                                attribute_value is None:
                            print("** value missing **")
                            return
                    attr_name = attribute_name
                    attr_value = attribute_value
                    obj = models.storage.all()[key]
                    try:
                        attr_value = eval(attr_value)
                    except (NameError, SyntaxError):
                        pass
                    setattr(obj, attr_name, attr_value)
        models.storage.save()


if __name__ == "__main__":
    FootballScoutCommand().cmdloop()
