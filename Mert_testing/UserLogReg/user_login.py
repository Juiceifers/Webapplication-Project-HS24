from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Generate a random secret key
secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key  # Use a secure key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # Database URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login.html"  # Redirect to login page if not logged in

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def home():
    return render_template("index.html", name=current_user.username)

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for("index.html"))
            else:
                flash("Invalid password")
        else:
            flash("User not found")
        
    return render_template("login.html")

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            flash("User already exists")
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for("login.html"))
        
    return render_template("register.html")

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.html"))

# Run the app
if __name__ == "__main__":
    db.create_all()  # Create database and tables
    app.run(debug=True)
