from flask import request, jsonify, Blueprint
import pymysql
from config import DB_CONFIG
from auth import token_required

products_bp = Blueprint('products', __name__)

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor
    )

# Get all products or filter by category
@products_bp.route('/', methods=['GET'])
def get_products():
    category_id = request.args.get('category_id', None)
    search = request.args.get('search', None)
    sort_by = request.args.get('sort', 'id')
    sort_order = request.args.get('order', 'asc')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Start building query
        query = """
            SELECT p.*, c.name as category_name 
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.stock > 0
        """
        params = []
        
        # Add category filter if provided
        if category_id:
            query += " AND p.category_id = %s"
            params.append(category_id)
            
        # Add search filter if provided
        if search:
            query += " AND (p.name LIKE %s OR p.description LIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])
            
        # Add sorting
        valid_sort_fields = ['id', 'name', 'price', 'created_at']
        valid_sort_orders = ['asc', 'desc']
        
        if sort_by not in valid_sort_fields:
            sort_by = 'id'
        if sort_order.lower() not in valid_sort_orders:
            sort_order = 'asc'
            
        query += f" ORDER BY p.{sort_by} {sort_order}"
        
        cursor.execute(query, params)
        products = cursor.fetchall()
        
        return jsonify({"status": "success", "data": products})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Get product by ID
@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get product details
        cursor.execute("""
            SELECT p.*, c.name as category_name 
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.id = %s
        """, (product_id,))
        
        product = cursor.fetchone()
        
        if not product:
            return jsonify({"status": "error", "message": "Product not found"}), 404
        
        # Get product reviews
        cursor.execute("""
            SELECT r.id, r.rating, r.comment, r.created_at, u.username
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.product_id = %s
            ORDER BY r.created_at DESC
        """, (product_id,))
        
        reviews = cursor.fetchall()
        product['reviews'] = reviews
        
        # Calculate average rating
        if reviews:
            avg_rating = sum(review['rating'] for review in reviews) / len(reviews)
            product['avg_rating'] = round(avg_rating, 1)
        else:
            product['avg_rating'] = 0
            
        return jsonify({"status": "success", "data": product})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Get all categories
@products_bp.route('/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        
        return jsonify({"status": "success", "data": categories})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Add product review
@products_bp.route('/<int:product_id>/reviews', methods=['POST'])
@token_required
def add_review(current_user, product_id):
    data = request.json
    
    if not data or 'rating' not in data or 'order_id' not in data:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
    # Validate rating
    rating = int(data['rating'])
    if rating < 1 or rating > 5:
        return jsonify({'status': 'error', 'message': 'Rating must be between 1 and 5'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if product exists
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
            
        # Check if order exists and belongs to user
        cursor.execute(
            "SELECT * FROM orders WHERE id = %s AND user_id = %s", 
            (data['order_id'], current_user['id'])
        )
        
        order = cursor.fetchone()
        if not order:
            return jsonify({'status': 'error', 'message': 'Order not found or not authorized'}), 404
            
        # Check if user already reviewed this product for this order
        cursor.execute(
            "SELECT * FROM reviews WHERE product_id = %s AND user_id = %s AND order_id = %s",
            (product_id, current_user['id'], data['order_id'])
        )
        
        if cursor.fetchone():
            return jsonify({'status': 'error', 'message': 'You have already reviewed this product for this order'}), 409
            
        # Add review
        cursor.execute(
            "INSERT INTO reviews (product_id, user_id, order_id, rating, comment) VALUES (%s, %s, %s, %s, %s)",
            (product_id, current_user['id'], data['order_id'], rating, data.get('comment', ''))
        )
        
        conn.commit()
        
        return jsonify({'status': 'success', 'message': 'Review added successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close() 