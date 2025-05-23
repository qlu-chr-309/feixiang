from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from config import DB_CONFIG

# Import blueprints
from auth import auth_bp
from products import products_bp
from orders import orders_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(orders_bp, url_prefix='/api/orders')

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor
    )

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "飞享无人机服务平台 API",
        "version": "1.0.0",
        "endpoints": {
            "auth": ["/api/auth/register", "/api/auth/login", "/api/auth/profile"],
            "products": ["/api/products", "/api/products/<id>", "/api/products/categories"],
            "orders": ["/api/orders", "/api/orders/<id>", "/api/orders/<id>/status", "/api/orders/<id>/cancel"]
        }
    })

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
