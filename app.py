from flask import Flask, render_template, request
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = 'lol'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(30), index=True, unique=True)
    password = db.Column(db.Unicode(30))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return "<User id: {0} and name: {1}>".format(self.id, self.name)


class RegisterForm(Form):
    name = StringField(label='Name')
    password = PasswordField(label='Password')
    submit = SubmitField(label='Login')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = RegisterForm()

    if request.method == 'POST':
        name = form.name.data
        password = form.password.data
        user = User(name, password)
        db.session.add(user)
        db.session.commit()
        return render_template("index.html")

    return render_template("login.html", form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", debug=True)
