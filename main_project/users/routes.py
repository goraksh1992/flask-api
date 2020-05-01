from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from main_project.users.models import User
import uuid
from main_project import db, app
import jwt
import datetime
from main_project.users.utils import token_required

users = Blueprint('users', __name__)


@users.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({"message": "Not authorized user"})

    users = User.query.all()
    print(users)
    user_data = []
    for user in users:
        user_dict = {}
        user_dict['name'] = user.name
        user_dict['public_id'] = user.public_id
        user_dict['password'] = user.password
        user_dict['admin'] = user.admin
        user_data.append(user_dict)

    return jsonify({"users": user_data})


@users.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=data['admin'])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "New user added successfully."})


@users.route('/user/<int:user_id>', methods=['GET'])
@token_required
def get_one_user(current_user, user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "No user found."})

    user_data = {"name": user.name, "public_id": user.public_id, "password": user.password, "admin": user.admin}
    return jsonify({"user": user_data})


@users.route('/user/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    user = User.query.get(user_id)
    data = request.get_json()

    if not user:
        return jsonify({"message": "No user found."})

    user.name = data['name']
    user.admin = data['admin']
    db.session.commit()

    return jsonify({"message": "User details updated."})


@users.route('/user/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "No user found."})
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted."})


@users.route('/user/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Content not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Content not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({"token": token.decode('utf-8')})

    return make_response('Content not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
