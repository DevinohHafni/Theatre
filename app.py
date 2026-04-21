"""
Theater Management System - Flask Backend
Run: python app.py
Requires: pip install flask flask-cors mysql-connector-python
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import mysql.connector
from mysql.connector import Error
from datetime import date, datetime
import decimal

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    import os
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

# ──────────────────────────────────────────────
# Database Configuration — update as needed
# ──────────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',          # ← change to your MySQL password
    'database': 'theater_db',
    'port': 3306
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def serialize(row):
    """Convert MySQL row values to JSON-safe types."""
    import datetime as dt
    result = {}
    for key, val in row.items():
        if isinstance(val, decimal.Decimal):
            result[key] = float(val)
        elif isinstance(val, (date, datetime)):
            result[key] = val.isoformat()
        elif isinstance(val, dt.timedelta):
            # MySQL TIME columns come back as timedelta
            total_seconds = int(val.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            result[key] = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        else:
            result[key] = val
    return result


def query(sql, params=None, fetchone=False, commit=False):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, params or ())
        if commit:
            conn.commit()
            return cur.lastrowid
        if fetchone:
            row = cur.fetchone()
            return serialize(row) if row else None
        return [serialize(r) for r in cur.fetchall()]
    finally:
        cur.close()
        conn.close()


# ──────────────────────────────────────────────
# Health
# ──────────────────────────────────────────────
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})


# ══════════════════════════════════════════════
# THEATERS
# ══════════════════════════════════════════════
@app.route('/api/theaters', methods=['GET'])
def get_theaters():
    rows = query("SELECT * FROM theaters ORDER BY name")
    return jsonify(rows)


@app.route('/api/theaters/<int:tid>', methods=['GET'])
def get_theater(tid):
    row = query("SELECT * FROM theaters WHERE id=%s", (tid,), fetchone=True)
    if not row:
        return jsonify({'error': 'Theater not found'}), 404
    return jsonify(row)


@app.route('/api/theaters', methods=['POST'])
def create_theater():
    d = request.json
    if not d or not d.get('name') or not d.get('total_seats'):
        return jsonify({'error': 'name and total_seats are required'}), 400
    lid = query(
        "INSERT INTO theaters (name, total_seats, description) VALUES (%s, %s, %s)",
        (d['name'], d['total_seats'], d.get('description', '')),
        commit=True
    )
    return jsonify({'id': lid, 'message': 'Theater created'}), 201


@app.route('/api/theaters/<int:tid>', methods=['PUT'])
def update_theater(tid):
    d = request.json
    query(
        "UPDATE theaters SET name=%s, total_seats=%s, description=%s WHERE id=%s",
        (d['name'], d['total_seats'], d.get('description', ''), tid),
        commit=True
    )
    return jsonify({'message': 'Theater updated'})


@app.route('/api/theaters/<int:tid>', methods=['DELETE'])
def delete_theater(tid):
    query("DELETE FROM theaters WHERE id=%s", (tid,), commit=True)
    return jsonify({'message': 'Theater deleted'})


# ══════════════════════════════════════════════
# MOVIES
# ══════════════════════════════════════════════
@app.route('/api/movies', methods=['GET'])
def get_movies():
    rows = query("SELECT * FROM movies ORDER BY title")
    return jsonify(rows)


@app.route('/api/movies/<int:mid>', methods=['GET'])
def get_movie(mid):
    row = query("SELECT * FROM movies WHERE id=%s", (mid,), fetchone=True)
    if not row:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(row)


@app.route('/api/movies', methods=['POST'])
def create_movie():
    d = request.json
    if not d or not d.get('title') or not d.get('duration_minutes'):
        return jsonify({'error': 'title and duration_minutes are required'}), 400
    lid = query(
        "INSERT INTO movies (title, genre, duration_minutes, language, rating, description) VALUES (%s,%s,%s,%s,%s,%s)",
        (d['title'], d.get('genre', ''), d['duration_minutes'],
         d.get('language', 'English'), d.get('rating', ''), d.get('description', '')),
        commit=True
    )
    return jsonify({'id': lid, 'message': 'Movie created'}), 201


@app.route('/api/movies/<int:mid>', methods=['PUT'])
def update_movie(mid):
    d = request.json
    query(
        "UPDATE movies SET title=%s, genre=%s, duration_minutes=%s, language=%s, rating=%s, description=%s WHERE id=%s",
        (d['title'], d.get('genre', ''), d['duration_minutes'],
         d.get('language', 'English'), d.get('rating', ''), d.get('description', ''), mid),
        commit=True
    )
    return jsonify({'message': 'Movie updated'})


@app.route('/api/movies/<int:mid>', methods=['DELETE'])
def delete_movie(mid):
    query("DELETE FROM movies WHERE id=%s", (mid,), commit=True)
    return jsonify({'message': 'Movie deleted'})


# ══════════════════════════════════════════════
# SHOWS
# ══════════════════════════════════════════════
@app.route('/api/shows', methods=['GET'])
def get_shows():
    rows = query("""
        SELECT s.*, m.title AS movie_title, m.genre, m.duration_minutes, m.rating,
               t.name AS theater_name, t.total_seats
        FROM shows s
        JOIN movies m ON s.movie_id = m.id
        JOIN theaters t ON s.theater_id = t.id
        ORDER BY s.show_date, s.show_time
    """)
    return jsonify(rows)


@app.route('/api/shows/<int:sid>', methods=['GET'])
def get_show(sid):
    row = query("""
        SELECT s.*, m.title AS movie_title, m.genre, m.duration_minutes, m.rating,
               t.name AS theater_name, t.total_seats
        FROM shows s
        JOIN movies m ON s.movie_id = m.id
        JOIN theaters t ON s.theater_id = t.id
        WHERE s.id=%s
    """, (sid,), fetchone=True)
    if not row:
        return jsonify({'error': 'Show not found'}), 404
    return jsonify(row)


@app.route('/api/shows', methods=['POST'])
def create_show():
    d = request.json
    required = ['movie_id', 'theater_id', 'show_date', 'show_time', 'ticket_price']
    if not d or any(k not in d for k in required):
        return jsonify({'error': f'Required: {required}'}), 400

    # Get theater capacity for available_seats
    theater = query("SELECT total_seats FROM theaters WHERE id=%s", (d['theater_id'],), fetchone=True)
    if not theater:
        return jsonify({'error': 'Theater not found'}), 404

    lid = query(
        "INSERT INTO shows (movie_id, theater_id, show_date, show_time, ticket_price, available_seats) VALUES (%s,%s,%s,%s,%s,%s)",
        (d['movie_id'], d['theater_id'], d['show_date'], d['show_time'],
         d['ticket_price'], theater['total_seats']),
        commit=True
    )
    return jsonify({'id': lid, 'message': 'Show created'}), 201


@app.route('/api/shows/<int:sid>', methods=['PUT'])
def update_show(sid):
    d = request.json
    query(
        "UPDATE shows SET movie_id=%s, theater_id=%s, show_date=%s, show_time=%s, ticket_price=%s, status=%s WHERE id=%s",
        (d['movie_id'], d['theater_id'], d['show_date'], d['show_time'],
         d['ticket_price'], d.get('status', 'active'), sid),
        commit=True
    )
    return jsonify({'message': 'Show updated'})


@app.route('/api/shows/<int:sid>', methods=['DELETE'])
def delete_show(sid):
    query("DELETE FROM shows WHERE id=%s", (sid,), commit=True)
    return jsonify({'message': 'Show deleted'})


# ══════════════════════════════════════════════
# CUSTOMERS
# ══════════════════════════════════════════════
@app.route('/api/customers', methods=['GET'])
def get_customers():
    rows = query("SELECT * FROM customers ORDER BY name")
    return jsonify(rows)


@app.route('/api/customers/<int:cid>', methods=['GET'])
def get_customer(cid):
    row = query("SELECT * FROM customers WHERE id=%s", (cid,), fetchone=True)
    if not row:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify(row)


@app.route('/api/customers', methods=['POST'])
def create_customer():
    d = request.json
    if not d or not d.get('name') or not d.get('email'):
        return jsonify({'error': 'name and email are required'}), 400
    # Check duplicate email
    existing = query("SELECT id FROM customers WHERE email=%s", (d['email'],), fetchone=True)
    if existing:
        return jsonify({'error': 'Email already registered'}), 409
    lid = query(
        "INSERT INTO customers (name, email, phone) VALUES (%s,%s,%s)",
        (d['name'], d['email'], d.get('phone', '')),
        commit=True
    )
    return jsonify({'id': lid, 'message': 'Customer created'}), 201


@app.route('/api/customers/<int:cid>', methods=['PUT'])
def update_customer(cid):
    d = request.json
    query(
        "UPDATE customers SET name=%s, email=%s, phone=%s WHERE id=%s",
        (d['name'], d['email'], d.get('phone', ''), cid),
        commit=True
    )
    return jsonify({'message': 'Customer updated'})


@app.route('/api/customers/<int:cid>', methods=['DELETE'])
def delete_customer(cid):
    query("DELETE FROM customers WHERE id=%s", (cid,), commit=True)
    return jsonify({'message': 'Customer deleted'})


# ══════════════════════════════════════════════
# BOOKINGS
# ══════════════════════════════════════════════
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    rows = query("""
        SELECT b.*, c.name AS customer_name, c.email AS customer_email,
               m.title AS movie_title, t.name AS theater_name,
               s.show_date, s.show_time, s.ticket_price
        FROM bookings b
        JOIN customers c ON b.customer_id = c.id
        JOIN shows s ON b.show_id = s.id
        JOIN movies m ON s.movie_id = m.id
        JOIN theaters t ON s.theater_id = t.id
        ORDER BY b.booked_at DESC
    """)
    return jsonify(rows)


@app.route('/api/bookings/<int:bid>', methods=['GET'])
def get_booking(bid):
    row = query("""
        SELECT b.*, c.name AS customer_name, c.email AS customer_email,
               m.title AS movie_title, t.name AS theater_name,
               s.show_date, s.show_time, s.ticket_price
        FROM bookings b
        JOIN customers c ON b.customer_id = c.id
        JOIN shows s ON b.show_id = s.id
        JOIN movies m ON s.movie_id = m.id
        JOIN theaters t ON s.theater_id = t.id
        WHERE b.id=%s
    """, (bid,), fetchone=True)
    if not row:
        return jsonify({'error': 'Booking not found'}), 404
    return jsonify(row)


@app.route('/api/bookings', methods=['POST'])
def create_booking():
    d = request.json
    required = ['show_id', 'customer_id', 'num_seats']
    if not d or any(k not in d for k in required):
        return jsonify({'error': f'Required: {required}'}), 400

    num_seats = int(d['num_seats'])
    if num_seats < 1:
        return jsonify({'error': 'num_seats must be at least 1'}), 400

    show = query("SELECT * FROM shows WHERE id=%s", (d['show_id'],), fetchone=True)
    if not show:
        return jsonify({'error': 'Show not found'}), 404
    if show['status'] != 'active':
        return jsonify({'error': 'Show is not active'}), 400
    if show['available_seats'] < num_seats:
        return jsonify({'error': f"Only {show['available_seats']} seats available"}), 400

    total = float(show['ticket_price']) * num_seats

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO bookings (show_id, customer_id, num_seats, total_amount) VALUES (%s,%s,%s,%s)",
            (d['show_id'], d['customer_id'], num_seats, total)
        )
        booking_id = cur.lastrowid
        cur.execute(
            "UPDATE shows SET available_seats = available_seats - %s WHERE id=%s",
            (num_seats, d['show_id'])
        )
        conn.commit()
        return jsonify({'id': booking_id, 'total_amount': total, 'message': 'Booking confirmed'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route('/api/bookings/<int:bid>/cancel', methods=['PUT'])
def cancel_booking(bid):
    booking = query("SELECT * FROM bookings WHERE id=%s", (bid,), fetchone=True)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    if booking['booking_status'] == 'cancelled':
        return jsonify({'error': 'Already cancelled'}), 400

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE bookings SET booking_status='cancelled' WHERE id=%s", (bid,))
        cur.execute(
            "UPDATE shows SET available_seats = available_seats + %s WHERE id=%s",
            (booking['num_seats'], booking['show_id'])
        )
        conn.commit()
        return jsonify({'message': 'Booking cancelled and seats restored'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route('/api/bookings/<int:bid>', methods=['DELETE'])
def delete_booking(bid):
    booking = query("SELECT * FROM bookings WHERE id=%s", (bid,), fetchone=True)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    # Restore seats if booking was confirmed
    if booking['booking_status'] == 'confirmed':
        query(
            "UPDATE shows SET available_seats = available_seats + %s WHERE id=%s",
            (booking['num_seats'], booking['show_id']),
            commit=True
        )
    query("DELETE FROM bookings WHERE id=%s", (bid,), commit=True)
    return jsonify({'message': 'Booking deleted'})


# ══════════════════════════════════════════════
# DASHBOARD STATS
# ══════════════════════════════════════════════
@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_movies = query("SELECT COUNT(*) AS c FROM movies", fetchone=True)['c']
    total_theaters = query("SELECT COUNT(*) AS c FROM theaters", fetchone=True)['c']
    total_shows = query("SELECT COUNT(*) AS c FROM shows WHERE status='active'", fetchone=True)['c']
    total_customers = query("SELECT COUNT(*) AS c FROM customers", fetchone=True)['c']
    total_bookings = query("SELECT COUNT(*) AS c FROM bookings WHERE booking_status='confirmed'", fetchone=True)['c']
    revenue_row = query("SELECT COALESCE(SUM(total_amount),0) AS r FROM bookings WHERE booking_status='confirmed'", fetchone=True)
    revenue = float(revenue_row['r'])

    return jsonify({
        'total_movies': total_movies,
        'total_theaters': total_theaters,
        'active_shows': total_shows,
        'total_customers': total_customers,
        'total_bookings': total_bookings,
        'total_revenue': revenue
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
