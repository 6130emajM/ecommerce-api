from flask import Blueprint, request, jsonify
from app import db
from models.user import User
from schemas.user_schema import UserSchema

users_bp = Blueprint('users', __name__, url_prefix='/users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user)

@users_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], address=data.get('address', ''), email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.address = data.get('address', user.address)
    user.email = data.get('email', user.email)
    db.session.commit()
    return user_schema.jsonify(user)

@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
