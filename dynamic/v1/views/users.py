#!/usr/bin/python3
"""
View module for handling User objects
"""

from flask import Flask, jsonify, request, abort
from dynamic.v1.views import app_views
from models import storage, User, UserRoleEnum, Club, Player, Scout
from console import FootballScoutCommand

@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    # users = User.query.all()
    users = storage.all(User).values()
    users_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': (user.first_name or '') + ' ' + (user.last_name or ''),
            'role': user.role.value if user.role else None  # Convert the enum to its value and Handle NoneType for user.role
        }
        users_list.append(user_data)
    return jsonify(users_list)
    # return jsonify([user.to_dict() for user in users])

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    # user_list = []
    # for attr in user:
    user_data = {
        'id': user.id,
        'name': (user.first_name or '') + ' ' + (user.last_name or ''),
        'role': user.role.value if user.role else None  # Convert the enum to its value and Handle NoneType for user.role
    }
    return jsonify(user_data)
    # user_list.append(user_data)
    # return jsonify(user_list)

    # return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a User object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    if 'first_name' not in data:
        abort(400, description="Missing first_name")
    if 'last_name' not in data:
        abort(400, description="Missing last_name")
    
    # Ensure role is set to 'ordinary' if not provided
    role = data.get('role', 'ordinary')
    if role not in ['ordinary', 'player', 'scout']:
        abort(400, description="Invalid role")

    # Create the User object with proper role
    data['role'] = UserRoleEnum[role]  # Convert role string to UserRoleEnum

    user = User(**data)
    user.save()

    user_data = {
        'id': user.id,
        'name': (user.first_name or '') + ' ' + (user.last_name or ''),
        'role': user.role.value if user.role else None  # Convert the enum to its value and Handle NoneType for user.role
    }
    return jsonify(user_data), 201

    # return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()

    # Check if 'role' is in the update data
    if 'role' in data:
        new_role = data['role']
        if new_role not in ['scout', 'player']:
            abort(400, description="Invalid role")

    # Check if 'club_id' is provided and valid
    if 'club_id' in data:
        club_id = data['club_id']
        club = storage.get(Club, club_id)
        if not club:
            abort(400, description=f"Club with ID {club_id} not found")
        
        # Assign club_id to user
        user.club_id = club_id

    try:
        # Update user role if 'role' is provided
        if 'role' in data:
            # Use the role_switch method from console.py to switch roles
            FootballScoutCommand().do_role_switch(f"{user_id} {new_role} {club_id}")

            # Retrieve the new role instance
            if new_role == 'player':
                # new_instance = storage.session.query(Player).filter_by(id=user_id).first()
                new_instance = storage.get(Player, user_id)
                if not new_instance:
                    abort(404, description="New Player instance not found")
                player_data = {
                    'id': new_instance.id,
                    'name': (new_instance.first_name or '') + ' ' + (new_instance.last_name or ''),
                    'email': new_instance.email,
                    'height': new_instance.height,
                    'weight': new_instance.weight,
                    'date_of_birth': new_instance.date_of_birth,
                    'club_id': new_instance.club_id,
                    'created_at': new_instance.created_at,
                    'updated_at': new_instance.updated_at
                }
                return jsonify(player_data), 200

            elif new_role == 'scout':
                # new_instance = storage.session.query(Scout).filter_by(id=user_id).first()
                new_instance = storage.get(Scout, user_id)
                if not new_instance:
                    abort(404, description="New Scout instance not found")
                scout_data = {
                    'id': new_instance.id,
                    'name': (new_instance.first_name or '') + ' ' + (new_instance.last_name or ''),
                    'email': new_instance.email,
                    'club_id': new_instance.club_id,
                    'created_at': new_instance.created_at,
                    'updated_at': new_instance.updated_at
                }
                return jsonify(scout_data), 200

        # except Exception as e:
        #    abort(400, description=f"Failed to switch role: {str(e)}")

    # Check if 'club_id' is provided and valid
    # if 'club_id' in data:
    #    club_id = data['club_id']
    #    club = storage.get(Club, club_id)
    #    if not club:
    #        abort(400, description=f"Club with ID {club_id} not found")

        # Assign club_id to user
        # user.club_id = club_id
    
        # Update other attributes
        # ignore_keys = ['id', 'email', 'created_at', 'updated_at', 'role', 'club_id']
        # for key, value in data.items():
        #    if key not in ignore_keys:
        #        setattr(user, key, value)

        # user.save()

    except Exception as e:
        storage.rollback()  # Ensure the session is rolled back
        abort(400, description=f"Failed to update user: {str(e)}")

    # If no role change, return updated user info
    # user_data = {
    #    'id': user.id,
    #    'name': (user.first_name or '') + ' ' + (user.last_name or ''),
    #    'role': user.role.value if user.role else None,  # Convert the enum to its value and Handle NoneType for user.role
    #    'club_id': user.club_id
    # }
    # return jsonify(user_data), 200

#@app_views.route('/users/<user_id>', methods=['PUT'])
#def update_user(user_id):
#    """Updates a User object"""
#    user = storage.get(User, user_id)
#    if not user:
#        abort(404)
#    if not request.get_json():
#        abort(400, description="Not a JSON")
#    data = request.get_json()
#    
#    # Upgrade user to scout or player
#    # if 'role' in data:
#    #    role = data['role']
#    #    if role == 'scout':
#    #        # Check if user is already a scout
#    #        if not isinstance(user, Scout):
#    #            scout = Scout(**user.to_dict())
#    #            scout.save()
#    #            user.delete()
#    #            storage.save()
#    #            return jsonify(scout.to_dict()), 200
#    #        else:
#    #            return jsonify(user.to_dict()), 200
#    #    elif role == 'player':
#            # Check if user is already a player
#    #        if not isinstance(user, Player):
#    #            player = Player(**user.to_dict())
#    #            player.save()
#    #            user.delete()
#    #            storage.save()
#    #            return jsonify(player.to_dict()), 200
#    #        else:
#    #            return jsonify(user.to_dict()), 200
#    #    else:
#    #        abort(400, description="Invalid role")
#    
#    # Upgrade user to scout or player
#    if 'role' in data:
#        if data['role'] not in UserRoleEnum._member_names_:
#        # if data['role'] not in ['ordinary', 'player', 'scout']:
#            return jsonify({"error": "Invalid role"}), 400
#        # user.role = data['role']
#
#        # user.role = UserRoleEnum[data['role']]  # Convert string to UserRoleEnum
#        
#        try:
#            user.switch_role(data['role'])
#            return jsonify(user.to_dict()), 200
#        except ValueError as e:
#            abort(400, description=str(e))
#
#    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
#    for key, value in data.items():
#        if key not in ignore_keys:
#            setattr(user, key, value)
#    user.save()
#    return jsonify(user.to_dict()), 200

