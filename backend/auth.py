from flask import request, jsonify, Blueprint
import pymysql
import bcrypt
import jwt
import datetime
from config import DB_CONFIG, JWT_SECRET
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor
    )

# JWT token verification decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'status': 'error', 'message': 'Token is missing'}), 401
        
        try:
            # Verify token
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            
            # Get user from database
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, username, email, role FROM users WHERE id = %s", (data['user_id'],))
            current_user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not current_user:
                return jsonify({'status': 'error', 'message': 'User not found'}), 401
                
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 401
            
        return f(current_user, *args, **kwargs)
        
    return decorated

# Register new user
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    # Hash the password
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", 
                      (data['username'], data['email']))
        
        if cursor.fetchone():
            return jsonify({'status': 'error', 'message': 'Username or email already exists'}), 409
            
        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)",
            (data['username'], hashed_password, data['email'], data.get('phone', ''))
        )
        
        conn.commit()
        
        # Get user ID for token
        user_id = cursor.lastrowid
        
        # Generate token
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, JWT_SECRET, algorithm="HS256")
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': user_id,
                'username': data['username'],
                'email': data['email'],
                'role': 'customer'
            }
        })
        
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
        
    finally:
        cursor.close()
        conn.close()

# Login user
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'status': 'error', 'message': 'Missing username or password'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Find user by username
        cursor.execute("SELECT * FROM users WHERE username = %s", (data['username'],))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
            
        # Check password
        if bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
            # Generate token
            token = jwt.encode({
                'user_id': user['id'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
            }, JWT_SECRET, algorithm="HS256")
            
            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            })
        else:
            return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
        
    finally:
        cursor.close()
        conn.close()

# Get user profile
@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({
        'status': 'success',
        'data': {
            'id': current_user['id'],
            'username': current_user['username'],
            'email': current_user['email'],
            'role': current_user['role']
        }
    }) 