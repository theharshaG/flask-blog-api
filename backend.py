from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------
# APP SETUP
# -------------------------
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret123'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# -------------------------
# MODELS
# -------------------------

# USER TABLE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

    # One user -> many posts
    posts = db.relationship('Post', backref='user', lazy=True)


# POST TABLE
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)

    # Foreign key (connect to user)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Create DB
with app.app_context():
    db.create_all()

# -------------------------
# HOME
# -------------------------
@app.route('/')
def home():
    return "Blog API Running"

# -------------------------
# REGISTER
# -------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check existing user
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "User already exists"})

    user = User(
        username=data['username'],
        password=generate_password_hash(data['password'])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"})

# -------------------------
# LOGIN
# -------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data['username']).first()

    if not user:
        return jsonify({"error": "User not found"})

    if check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({"message": "Login success", "token": token})

    return jsonify({"error": "Invalid password"})

# -------------------------
# CREATE POST
# -------------------------
@app.route('/post', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()

    post = Post(
        title=data['title'],
        content=data['content'],
        user_id=user_id
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created"})

# -------------------------
# GET POSTS (PAGINATION)
# -------------------------
@app.route('/posts', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = 2

    posts = Post.query.paginate(page=page, per_page=per_page)

    result = []

    for p in posts.items:
        result.append({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "author": p.user.username
        })

    return jsonify({
        "page": page,
        "data": result
    })

# -------------------------
# UPDATE POST
# -------------------------
@app.route('/post/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
    data = request.get_json()
    user_id = get_jwt_identity()

    post = Post.query.get(id)

    if not post:
        return jsonify({"error": "Post not found"})

    if post.user_id != user_id:
        return jsonify({"error": "Not authorized"})

    post.title = data['title']
    post.content = data['content']

    db.session.commit()

    return jsonify({"message": "Post updated"})

# -------------------------
# DELETE POST
# -------------------------
@app.route('/post/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    user_id = get_jwt_identity()

    post = Post.query.get(id)

    if not post:
        return jsonify({"error": "Post not found"})

    if post.user_id != user_id:
        return jsonify({"error": "Not authorized"})

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted"})

# -------------------------
# RUN
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
