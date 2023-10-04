from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_babel import Babel
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.secret_key = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/test-crud-db"

db = SQLAlchemy(app)
babel = Babel(app)

admin = Admin(app, name="Admin")


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, doc="Name")

    def __str__(self):
        return self.name


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, doc="Name")
    login = db.Column(db.String(64), nullable=False, unique=True, doc="Login")
    password = db.Column(db.String(128), nullable=False, doc="Password")

    roles = db.relationship(Roles, secondary="user_roles", backref="users")


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, doc="User")
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False, doc="Role")
	

class UsersView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True

    form_columns = ['name', 'login', 'password', 'roles']

    column_hide_backref = False
	

class RolesView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True

    form_columns = ['name']


admin.add_view(UsersView(Users, db.session))
admin.add_view(RolesView(Roles, db.session))


@app.route("/")
@app.route("/index")
def index():
    return '<h1><a href="/admin">Admin panel</a></h1>'


if __name__ == "__main__":
    app.run(debug=True)