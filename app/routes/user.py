from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, db, UserRole
from app.schemas import user_schema, users_schema

user = Blueprint('user', __name__)

@user.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Admin access required'}), 403
    
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

@user.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def user_operations(user_id):
    current_user = User.query.get(get_jwt_identity())
    target_user = User.query.get(user_id)
    
    if not target_user:
        return jsonify({'message': 'User not found'}), 404
    
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        return jsonify(user_schema.dump(target_user)), 200
    
    
    elif request.method == 'PUT':
        if current_user.role == UserRole.ADMIN and  target_user.role == UserRole.ADMIN and current_user.id != user_id:
            return jsonify({'message': 'Admin cannot modify another admin\'s information'}), 403
        data = request.get_json()
        for key, value in data.items():
            if key != 'role' or (key == 'role' and current_user.role == UserRole.ADMIN):
                setattr(target_user, key, value)
        db.session.commit()
        return jsonify(user_schema.dump(target_user)), 200
    
    elif request.method == 'DELETE':
        if current_user.role == UserRole.ADMIN and  target_user.role == UserRole.ADMIN and current_user.id != user_id:
            return jsonify({'message': 'Admin cannot modify another admin\'s information'}), 403
        if current_user.role == UserRole.ADMIN:
            db.session.delete(target_user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'message': 'Admin access required for deletion'}), 403