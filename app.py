from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = 'carshowroom123'

# ---------- DB CONNECTION ----------
def get_db():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="raj2005"
    )
    return conn


# ---------- HOME ----------
@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM cars")
    cars = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', cars=cars)


# ---------- AUTH ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        flash('Invalid credentials!')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, 'user')",
                        (username, password, email))
            conn.commit()
            flash('Registered! Please login.')
            return redirect(url_for('login'))
        except:
            conn.rollback()
            flash('Username already exists!')
        finally:
            cur.close()
            conn.close()
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------- USER DASHBOARD ----------
@app.route('/user/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM cars")
    cars = cur.fetchall()
    cur.execute("SELECT b.*, c.brand, c.model FROM bookings b JOIN cars c ON b.car_id=c.id WHERE b.user_id=%s", (session['user_id'],))
    bookings = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('user_dashboard.html', cars=cars, bookings=bookings)


@app.route('/user/book/<int:car_id>', methods=['POST'])
def book_car(car_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO bookings (user_id, car_id, status) VALUES (%s, %s, 'Pending')",
                (session['user_id'], car_id))
    conn.commit()
    cur.close()
    conn.close()
    flash('Car booked successfully!')
    return redirect(url_for('user_dashboard'))


# ---------- ADMIN DASHBOARD ----------
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM cars")
    cars = cur.fetchall()
    cur.execute("SELECT b.*, u.username, c.brand, c.model FROM bookings b JOIN users u ON b.user_id=u.id JOIN cars c ON b.car_id=c.id ORDER BY b.booked_at DESC")
    bookings = cur.fetchall()
    cur.execute("SELECT id, username, email, role FROM users WHERE role='user' ORDER BY id")
    users = cur.fetchall()
    user_count = len(users)
    cur.close()
    conn.close()
    return render_template('admin_dashboard.html', cars=cars, bookings=bookings, user_count=user_count, users=users)


@app.route('/admin/add_car', methods=['POST'])
def add_car():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    brand = request.form['brand']
    model = request.form['model']
    year = request.form['year']
    price = request.form['price']
    color = request.form['color']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO cars (brand, model, year, price, color) VALUES (%s, %s, %s, %s, %s)",
                (brand, model, year, price, color))
    conn.commit()
    cur.close()
    conn.close()
    flash('Car added!')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete_car/<int:car_id>')
def delete_car(car_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM bookings WHERE car_id=%s", (car_id,))
    cur.execute("DELETE FROM cars WHERE id=%s", (car_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Car deleted!')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/update_booking/<int:booking_id>/<status>')
def update_booking(booking_id, status):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE bookings SET status=%s WHERE id=%s", (status, booking_id))
    conn.commit()
    cur.close()
    conn.close()
    flash(f'Booking {status}!')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
