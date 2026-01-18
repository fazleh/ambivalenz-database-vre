from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from neo4j import GraphDatabase
from werkzeug.security import generate_password_hash

# --- Flask setup
app = Flask(__name__)
app.secret_key = 'super-secret-key'

# --- Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- Neo4j config
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        with driver.session() as session:
            # Check if user already exists
            result = session.run(
                "MATCH (u:User {username: $username}) RETURN u",
                {"username": username}
            )
            if result.single():
                flash("Username already taken")
                return redirect(url_for('register'))

            # Create the user
            session.run(
                """
                CREATE (u:User {
                    id: toInteger(timestamp()),
                    username: $username,
                    password_hash: $password_hash
                })
                """,
                {"username": username, "password_hash": password_hash}
            )

            flash("Registration successful! You can now log in.")
            return redirect(url_for('login'))

    return render_template('register.html')


# --- User model
class User(UserMixin):
    def __init__(self, id_, username, password_hash):
        self.id = id_
        self.username = username
        self.password_hash = password_hash

# --- Load user from session
@login_manager.user_loader
def load_user(user_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User) WHERE u.id = $id RETURN u", {"id": int(user_id)}
        )
        record = result.single()
        if record:
            u = record["u"]
            return User(u["id"], u["username"], u["password_hash"])
    return None

# --- Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with driver.session() as session:
            result = session.run(
                "MATCH (u:User {username: $username}) RETURN u",
                {"username": username}
            )
            record = result.single()
            if record:
                u = record["u"]
                if check_password_hash(u["password_hash"], password):
                    user = User(u["id"], u["username"], u["password_hash"])
                    login_user(user)
                    return redirect(url_for('dashboard'))

        flash("Invalid username or password")
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html', username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Optional: Create a default user if none exists
def ensure_default_user():
    with driver.session() as session:
        result = session.run("MATCH (u:User {username: $username}) RETURN u", {"username": "admin"})
        if not result.single():
            hashed = generate_password_hash("secret")
            session.run(
                "CREATE (u:User {id: $id, username: $username, password_hash: $password_hash})",
                {"id": 1, "username": "admin", "password_hash": hashed}
            )

if __name__ == '__main__':
    ensure_default_user()
    app.run(debug=True)
