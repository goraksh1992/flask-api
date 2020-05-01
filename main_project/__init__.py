from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '1e7fd33a00c9b5b3f4351a402061c8ce'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


from main_project.users.routes import users
from main_project.todo.routes import todo

app.register_blueprint(users)
app.register_blueprint(todo)
