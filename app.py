from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from config import Config
from datetime import datetime
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm, PoemForm# For validation of html form submission
from flask_login import login_required, current_user

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# Database Models (Tables)
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    poems = db.relationship('Poem', backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

class Poem(db.Model):
    poem_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    text = db.Column(db.String(1200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"

# Routes (html)
@app.route("/") 
def home():
    return render_template("home.html")

@app.route("/read")
def read():
    poems = Poem.query.all()
    return render_template('read.html', poems=poems)

@app.route("/add", methods=['GET', 'POST'])
#@login_required()
def add_poem():
    form = PoemForm()
    if form.validate_on_submit():
        poem = Poem(title=form.title.data, text=form.text.data, user_id=1)#current_user)
        db.session.add(poem)
        db.session.commit()
        flash('Your poem has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('add.html', title='Add Poem',
                           form=form, legend='Add Poem')



@app.route("/registration", methods=["POST","GET"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}')
        return redirect(url_for('registration'))
    #result = request.form
    return render_template("registration.html",form=form)

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["email"]
        session["user"] = user
        return render_template("home.html")
    else:
        return render_template("login.html")

@app.route("/logout", methods=["POST","GET"])
def logout():
    session.pop("user",None)
    flash("Logged Out!")
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)