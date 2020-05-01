from flask import Blueprint, jsonify, request
from main_project.todo.models import Todo
from main_project.users.models import User
from main_project.users.utils import token_required
from main_project import db

todo = Blueprint('todo', __name__)


@todo.route('/todo', methods=['GET'])
@token_required
def get_all_todo(current_user):
    todos = Todo.query.all()

    todo_data = []
    for todo in todos:
        user = User.query.get(todo.user_id)
        t = {}
        t['text'] = todo.text
        t['complete'] = todo.complete
        t['user_id'] = todo.user_id
        t['name'] = user.name
        todo_data.append(t)

    return jsonify({"todo": todo_data})


@todo.route('/todo/<int:todo_id>', methods=['GET'])
def get_one_todo(current_user, todo_id):
    pass


@todo.route('/todo', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()

    todo = Todo(text=data['text'], complete=data['complete'], user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()
    return jsonify({"message": "Todo added."})


@todo.route('/todo/<int:todo_id>', method=['PUT'])
@token_required
def update_todo(current_user, todo_id):
    pass


