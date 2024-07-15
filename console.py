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

    def do_role_switch(self, line):
        """Switch user role to either 'scout' or 'player' with club_id"""
        args = shlex.split(line)
        if len(args) != 3:
            print("** usage: role_switch <user_id> <role> <club_id> **")
            return

        user_id, new_role, club_id = args
        if new_role not in ['scout', 'player']:
            print("** invalid role **")
            return

        # Find the user by ID
        key = f"User.{user_id}"
        user = storage.all().get(key)
        if not user:
            print(f"** no user found with id: {user_id} **")
            return

        # Create a new instance of the specified role with the same attributes
        if new_role == 'player':
            new_instance = Player(
                id=user.id,
                email=user.email,
                password=user.password,
                first_name=user.first_name,
                last_name=user.last_name,
                club_id=club_id
            )
        elif new_role == 'scout':
            new_instance = Scout(
                id=user.id,
                email=user.email,
                password=user.password,
                first_name=user.first_name,
                last_name=user.last_name,
                club_id=club_id
            )
        # else:
        #    print("** invalid role **")
        #    return

        # Set created_at and updated_at to current time
        new_instance.created_at = datetime.utcnow()
        new_instance.updated_at = datetime.utcnow()

        # Save the new instance and delete the old user instance
        try:
            # new_instance.save()
            # storage.delete(user)
            # storage.save()
            
            storage.new(new_instance)  # Register new instance
            storage.save()  # Commit the new instance to the database
            storage.delete(user)  # Mark the original user instance for deletion
            storage.save()  # Commit the deletion to the database

            print(f"User {user_id} switched to {new_role} role and original user deleted.")
        except Exception as e:
            storage.rollback()
            print(f"Error switching role: {str(e)}")

#    def do_role_switch(self, line):
#        """Switch user role to either 'scout' or 'player'"""
#        args = shlex.split(line)
#        if len(args) != 2:
#            print("** usage: role_switch <user_id> <role> **")
#            return
#
#        user_id, new_role = args
#        if new_role not in ['scout', 'player']:
#            print("** invalid role **")
#            return
#
#        # Find the user by ID
#        key = f"User.{user_id}"
#        user = storage.all().get(key)
#        if not user:
#            print(f"** no user found with id: {user_id} **")
#            return
#
#        # Delete the user
#        # storage.delete(user)
#
#        # Create a new instance of the specified role with the same attributes
#        if new_role == 'player':
#            new_instance = Player(
#                email=user.email,
#                password=user.password,
#                first_name=user.first_name,
#                last_name=user.last_name
#            )
#        elif new_role == 'scout':
#            new_instance = Scout(
#                email=user.email,
#                password=user.password,
#                first_name=user.first_name,
#                last_name=user.last_name
#            )
#        else:
#            print("** invalid role **")
#            return
#
#        new_instance.save()
#        print(f"User {user_id} switched to {new_role} role and original user deleted.")


#    def do_role_switch(self, line):
#        """Switch user role to either player or scout"""
#
#        try:
#            user1_id, new_role = line.split()
#        except ValueError:
#            print("** usage: role_switch <user_id> <new_role> **")
#            return
#
#        if new_role not in ['player', 'scout']:
#            print("** role must be either 'player' or 'scout' **")
#            return
#
#        print(f"Looking for user with ID: {user1_id} and switching to role: {new_role}")
#
#        from models import storage
#        users = storage.all("User")
#
#        user_to_switch = None
#        for user in users.values():
#            if user.id == user1_id:
#                user_to_switch = user
#                break
#
#        if not user_to_switch:
#            print("** no user found with the given ID **")
#            return
#
#        new_instance = None
#
#        # Create a new instance of the specified role with the same attributes
#        # if new_role == 'player':
#        #    new_instance = Player(
#        #        email=user.email,
#        #        password=user.password,
#        #        first_name=user.first_name,
#        #        last_name=user.last_name
#        #    )
#        # elif new_role == 'scout':
#        #    new_instance = Scout(
#        #        email=user.email,
#        #        password=user.password,
#        #        first_name=user.first_name,
#        #        last_name=user.last_name
#        #    )
#        # else:
#        #    print("** invalid role **")
#        #    return
#
#        # new_instance.save()
#        # print(f"User {user_id} switched to {new_role} role and original user deleted.")
#
#        if new_role == "player":
#            new_instance = Player(**user_to_switch.__dict__)
#        elif new_role == "scout":
#            new_instance = Scout(**user_to_switch.__dict__)
#
#        if new_instance:
#            new_instance.id = user_to_switch.id  # Retain the original user ID
#            new_instance.save()
#            print(f"User {user1_id} role switched to {new_role}")
#        
#            # Delete the original user
#        #    storage.delete(user_to_switch)
#            storage.save()
#            print(f"User {user1_id} switched to {new_role} role and original user deleted.")
#        else:
#            print("** error creating new instance **")

#    def do_role_switch(self, line):
#        """Switch user role to either player or scout"""
#
#        user1_id = line.strip()
#        print(f"Looking for user with ID: {user1_id}")
#
#        from models import storage
#        users_test = storage.all("User")
#        print(f"Total users found: {len(users_test)}")
#
#        # user1 = None
#        # for user_obj in users_test.values():
#        #    print(f"Checking user with ID: {user_obj.id}")
#        #    if user_obj.id == user1_id:
#        #        user1 = user_obj
#        #        break
#
#        # if not user1:
#        #    print("** No user found **")
#        #    return
#
#        # print(f"User found: {user1.first_name} {user1.last_name}")
#
#        args = shlex.split(line)
#        if len(args) != 2:
#            print("** Usage: role_switch <user_id> <new_role> **")
#            return
#        user_id = args[0]
#        new_role = args[1]
#
##        # Search for the user with the given ID
##        users = storage.all(User)
##        user_found = False
##
##        for user in users.values():
##            if user.id == user_id:
##                user_found = True
##                break
##        if not user_found:
##            print("** No user found **")
##
##        user_update = storage.get("User", user_id)
##        print("user_update: {}".format(user_update))
#
#
#
##        # Create new instance based on role
##        if new_role == "player":
##            new_instance = Player(
##                id=user.id,
##                email=user.email,
##                password=user.password,  # Inherit password
##                first_name=user.first_name,
##                last_name=user.last_name,
##            )
##        elif new_role == "scout":
##            new_instance = Scout(
##                id=user.id,
##                email=user.email,
##                password=user.password,  # Inherit password
##                first_name=user.first_name,
##                last_name=user.last_name,
##            )
##        # else:
##        #    print("** Invalid role **")
##        #    return
##
##        # Save the new instance
##        storage.new(new_instance)
##        storage.delete(user)
##        storage.save()
##        print("Role switched to", new_role)
#
#
#        # Search for the user with the given ID
#        users = storage.all(User)
#        user_found = False
#        for user in users.values():
#            if user.id == user_id:
#                user.role = new_role
#                user.save()
#                print(f"User {user_id} role switched to {new_role}")
#                user_found = True
#                break
#        if not user_found:
#            print("** No user found **")
#
#
#        # args = line.split()
##        args = shlex.split(line)
##        if len(args) != 2:
##            print("Usage: role_switch <user_id> <new_role>")
##            return
##
##        user_id, new_role = args[0], args[1]
##        if new_role not in ['player', 'scout']:
##            print("** Invalid role **")
##            return
##
##        from models import storage
##        user = storage.get("User", user_id)
##        # if user is None:
##        if not user:
##            print("** No user found **")
##            return
##
##        # Ensure the user has a password
##        # if user.password is None:
##        if not user.password:
##            print("** User password is missing **")
##            return
##
##        # Create new instance based on role
##        if new_role == "player":
##            new_instance = Player(
##                id=user.id,
##                email=user.email,
##                password=user.password,  # Inherit password
##                first_name=user.first_name,
##                last_name=user.last_name,
##            )
##        elif new_role == "scout":
##            new_instance = Scout(
##                id=user.id,
##                email=user.email,
##                password=user.password,  # Inherit password
##                first_name=user.first_name,
##                last_name=user.last_name,
##            )
##        # else:
##        #    print("** Invalid role **")
##        #    return
##
##        # Save the new instance
##        storage.new(new_instance)
##        storage.delete(user)
##        storage.save()
##        print("Role switched to", new_role)
#
#        # user_id, new_role = args[0], args[1]
#        # if new_role not in ['player', 'scout']:
#        #    print("Invalid role. Role must be either 'player' or 'scout'.")
#        #    return
#
#        # user = storage.get(User, user_id)
#        # if not user:
#        #    print(f"No user found with id {user_id}")
#        #    return
#
#        # Create new player or scout with existing user attributes and ID
#        # if new_role == 'player':
#        #    new_instance = Player(**user.to_dict())
#        # else:  # new_role == 'scout'
#        #    new_instance = Scout(**user.to_dict())
#
#        # Assign the same ID
#        # new_instance.id = user.id
#
#        # Update role in user object
#        # user.role = new_role
#
#        # Save new instance and updated user
#        # storage.new(new_instance)
#        # storage.save()
#
#        print(f"User {user_id} switched to {new_role} role.")


if __name__ == '__main__':
    FootballScoutCommand().cmdloop()
