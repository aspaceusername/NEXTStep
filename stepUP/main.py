from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "hello"  # Change this to a secure random key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))
    plano_treino_url = db.Column(db.String(500))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Home page route
@app.route('/')
def home():
    return render_template('index.html')


# About page route
@app.route('/about')
def about():
    return render_template('about.html')


# Example redirect
@app.route('/old-page')
def old_page():
    return redirect(url_for('home'))


# Example with parameters
@app.route('/user/<username>')
def user_profile(username):
    return render_template('profile.html', username=username)


# Admin Routes
@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


# Registration route
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if user already exists
        existing_user = users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!")
            return redirect(url_for("register"))

        # Create new user
        new_user = users(name, email, password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        found_user = users.query.filter_by(email=email).first()

        if found_user and found_user.check_password(password):
            session.permanent = True
            session["user"] = found_user.name
            session["email"] = found_user.email
            session["user_id"] = found_user._id
            flash("Login Successful!")
            return redirect(url_for("user"))
        else:
            flash("Invalid email or password!")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])  # Fixed: Added missing @
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user_dashboard.html", email=email, user=user)
    else:
        flash("You Are Not Logged In!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out", "info")
    session.pop("user", None)
    session.pop("email", None)
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route("/questionnaire")
def assessment():
    return render_template("questionnaire.html")
# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)