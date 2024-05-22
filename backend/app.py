import os
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import text

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

CORS(app, resources={r"/*": {"origins": "*"}})

db = SQLAlchemy(app)
jwt = JWTManager(app)

def wait_for_db():
    """Wait for the database to be available."""
    while True:
        try:
            # Try to perform a simple database operation
            db.session.execute(text('SELECT 1'))
            print("Database is ready!")
            break
        except Exception as e:
            print("Database is not ready, waiting...")
            time.sleep(5)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.before_request
def initialization_db():
    app.before_request_funcs[None].remove(initialization_db)
    with app.app_context():
        wait_for_db()
        db.create_all()
        print('Database Initilized!')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2', salt_length=16)
    print(hashed_password)
    new_user = User(username=data['username'], password=hashed_password)
    print('hit')
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            token = create_access_token(identity=user.id)
            return jsonify({'token': token})
        return jsonify({'message': 'Invalid credentials'}), 401
    except:
        return jsonify({'message': "something wrong!"}), 500

@app.route('/api/tasks', methods=['GET', 'POST'])
@jwt_required()
def manage_tasks():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        data = request.get_json()
        new_task = Task(description=data['description'], user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added successfully'})
    else:
        tasks = Task.query.filter_by(user_id=user_id).all()
        return jsonify([{'id': task.id, 'description': task.description} for task in tasks])

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    return jsonify({'message': 'Task not found'}), 404

@app.route('/check_db', methods=['GET'])
def check_db():
    try:
        # Try to perform a simple database operation
        db.session.execute(text('SELECT 1'))
        return jsonify({'message': 'Database connection successful'}), 200
    except Exception as e:
        return jsonify({'message': 'Database connection failed', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
