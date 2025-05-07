from flask import request, jsonify, Blueprint
import pymysql
from config import DB_CONFIG
from auth import token_required

orders_bp = Blueprint('orders', __name__)

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor
    )

# Create a new order
@orders_bp.route('/', methods=['POST'])
@token_required
def create_order(current_user):
    data = request.json
    
    if not data or not data.get('items') or not data.get('shipping_address'):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    # Validate order items
    if not isinstance(data['items'], list) or len(data['items']) == 0:
        return jsonify({'status': 'error', 'message': 'Order must contain at least one item'}), 400
    
    for item in data['items']:
        if 'product_id' not in item or 'quantity' not in item:
            return jsonify({'status': 'error', 'message': 'Invalid order item format'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Start transaction
        conn.begin()
        
        # Calculate total amount and check stock
        total_amount = 0
        order_items = []
        
        for item in data['items']:
            # Get product details and check stock
            cursor.execute(
                "SELECT id, name, price, stock FROM products WHERE id = %s", 
                (item['product_id'],)
            )
            
            product = cursor.fetchone()
            if not product:
                return jsonify({'status': 'error', 'message': f'Product ID {item["product_id"]} not found'}), 404
            
            if product['stock'] < item['quantity']:
                return jsonify({
                    'status': 'error', 
                    'message': f'Not enough stock for product {product["name"]}. Available: {product["stock"]}'
                }), 400
            
            # Calculate item total and add to order total
            item_total = product['price'] * item['quantity']
            total_amount += item_total
            
            # Save item details for later insertion
            order_items.append({
                'product_id': product['id'],
                'quantity': item['quantity'],
                'price': product['price']
            })
        
        # Create order
        cursor.execute(
            """
            INSERT INTO orders 
                (user_id, status, total_amount, shipping_address, payment_method, notes) 
            VALUES 
                (%s, %s, %s, %s, %s, %s)
            """,
            (
                current_user['id'],
                'pending', 
                total_amount,
                data['shipping_address'],
                data.get('payment_method', 'online'), 
                data.get('notes', '')
            )
        )
        
        order_id = cursor.lastrowid
        
        # Insert order items and update product stock
        for item in order_items:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, item['product_id'], item['quantity'], item['price'])
            )
            
            # Update product stock
            cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE id = %s",
                (item['quantity'], item['product_id'])
            )
        
        # Commit transaction
        conn.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Order created successfully',
            'data': {
                'order_id': order_id,
                'total_amount': total_amount
            }
        })
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Get user orders
@orders_bp.route('/', methods=['GET'])
@token_required
def get_user_orders(current_user):
    status = request.args.get('status', None)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Build query based on status filter
        query = "SELECT * FROM orders WHERE user_id = %s"
        params = [current_user['id']]
        
        if status:
            query += " AND status = %s"
            params.append(status)
            
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        orders = cursor.fetchall()
        
        # Get order items for each order
        for order in orders:
            cursor.execute(
                """
                SELECT oi.*, p.name, p.image
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = %s
                """,
                (order['id'],)
            )
            order['items'] = cursor.fetchall()
        
        return jsonify({'status': 'success', 'data': orders})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Get order details
@orders_bp.route('/<int:order_id>', methods=['GET'])
@token_required
def get_order_details(current_user, order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get order details
        cursor.execute(
            "SELECT * FROM orders WHERE id = %s AND user_id = %s", 
            (order_id, current_user['id'])
        )
        
        order = cursor.fetchone()
        if not order:
            return jsonify({'status': 'error', 'message': 'Order not found or not authorized'}), 404
        
        # Get order items
        cursor.execute(
            """
            SELECT oi.*, p.name, p.image, p.description
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
            """,
            (order_id,)
        )
        
        order['items'] = cursor.fetchall()
        
        return jsonify({'status': 'success', 'data': order})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Update order status (can be used for payment confirmation, etc.)
@orders_bp.route('/<int:order_id>/status', methods=['PUT'])
@token_required
def update_order_status(current_user, order_id):
    data = request.json
    
    if not data or 'status' not in data:
        return jsonify({'status': 'error', 'message': 'Status is required'}), 400
    
    # Validate status
    valid_statuses = ['pending', 'paid', 'shipped', 'delivered', 'cancelled']
    if data['status'] not in valid_statuses:
        return jsonify({'status': 'error', 'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if order exists and belongs to user (or user is admin)
        if current_user['role'] == 'admin':
            cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        else:
            cursor.execute(
                "SELECT * FROM orders WHERE id = %s AND user_id = %s", 
                (order_id, current_user['id'])
            )
        
        order = cursor.fetchone()
        if not order:
            return jsonify({'status': 'error', 'message': 'Order not found or not authorized'}), 404
        
        # Special handling for cancelled status - restore stock
        if data['status'] == 'cancelled' and order['status'] != 'cancelled':
            cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
            items = cursor.fetchall()
            
            for item in items:
                cursor.execute(
                    "UPDATE products SET stock = stock + %s WHERE id = %s",
                    (item['quantity'], item['product_id'])
                )
        
        # Update order status
        cursor.execute(
            "UPDATE orders SET status = %s WHERE id = %s",
            (data['status'], order_id)
        )
        
        conn.commit()
        
        return jsonify({'status': 'success', 'message': 'Order status updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Cancel order
@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@token_required
def cancel_order(current_user, order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if order exists and belongs to user
        cursor.execute(
            "SELECT * FROM orders WHERE id = %s AND user_id = %s", 
            (order_id, current_user['id'])
        )
        
        order = cursor.fetchone()
        if not order:
            return jsonify({'status': 'error', 'message': 'Order not found or not authorized'}), 404
        
        # Only pending orders can be cancelled
        if order['status'] != 'pending':
            return jsonify({'status': 'error', 'message': f'Cannot cancel order with status: {order["status"]}'}), 400
        
        # Start transaction
        conn.begin()
        
        # Get order items to restore stock
        cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
        items = cursor.fetchall()
        
        # Restore stock for each item
        for item in items:
            cursor.execute(
                "UPDATE products SET stock = stock + %s WHERE id = %s",
                (item['quantity'], item['product_id'])
            )
        
        # Update order status to cancelled
        cursor.execute(
            "UPDATE orders SET status = 'cancelled' WHERE id = %s",
            (order_id,)
        )
        
        conn.commit()
        
        return jsonify({'status': 'success', 'message': 'Order cancelled successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close() 