#!/usr/bin/env python3
""" console """

import cmd
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.country import Country
from models.club import Club
from models.position import Position
from models.post import Post
from models.comment import Comment
from models.like import Like
from models.user import User
from models.player import Player
from models.scout import Scout
import shlex  # for splitting the line along spaces except in double quotes

classes = {
    "BaseModel": BaseModel, "Country": Country, "Club": Club,
    "Player": Player, "Scout": Scout, "User": User, "Post": Post,
    "Like": Like, "Comment": Comment, "Position": Position
}


class FootballScoutCommand(cmd.Cmd):
    """ FootballScout1 console """
    prompt = '(football_scout) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """Overwriting the emptyline method"""
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """Creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except BaseException:
                        try:
                            value = float(value)
                        except BaseException:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Creates a new instance of a class"""
        # args = arg.split()
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        class_name = args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return False
        # if args[0] in classes:
        #    new_dict = self._key_value_parser(args[1:])

        # Check if attributes are provided
        if len(args) < 2:
            print("** missing attributes **")
            return False

        # Extract attributes from arguments
        attributes = {}
        for arg in args[1:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                attributes[key] = value.replace('_', ' ')

        try:
            instance = classes[class_name](**attributes)
            instance.save()
            print(instance.id)
        except Exception as e:
            print(f"Error creating instance: {str(e)}")


            # if 'name' not in new_dict:
            #    print("** missing name attribute **")
            #    return False

            # instance = classes[args[0]](**new_dict)

            # instance.save()
            # print(instance.id)
        # else:
        #   print("** class doesn't exist **")
        #   return False
        # print(instance.id)
        # instance.save()

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in storage.all():
                    print(storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in storage.all():
                    storage.all().pop(key)
                    storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = storage.all()
        elif args[0] in classes:
            obj_dict = storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            setattr(storage.all()[k], args[2], args[3])
                            storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
    FootballScoutCommand().cmdloop()
