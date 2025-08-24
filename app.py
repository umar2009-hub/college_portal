from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = "supersecretkey"   # for session

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Umar@2005'   # your MySQL password
app.config['MYSQL_DB'] = 'complaint_portal'

mysql = MySQL(app)
complaints = []

# ================= Routes =================

@app.route('/')
def home():
    return redirect(url_for('login'))
@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''  # message for errors
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        account = cursor.fetchone()

        if account:
            # store session values
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['name'] = account['name']
            session['role'] = account['role']

            # redirect based on role
            if account['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            # wrong credentials
            msg = 'Invalid email or password!'

    # render login page with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # ✅ Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("Email already exists. Please use another one.", "error")
            return redirect(url_for("register"))

        # ✅ Get the maximum user_id from table
        cursor.execute("SELECT MAX(user_id) AS max_id FROM users")
        result = cursor.fetchone()
        next_id = 1 if result['max_id'] is None else result['max_id'] + 1

        # ✅ Reset AUTO_INCREMENT to next_id
        cursor.execute("ALTER TABLE users AUTO_INCREMENT = %s", (next_id,))

        # ✅ Insert new record
        cursor.execute(
            'INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)',
            (name, email, password, role)
        )
        mysql.connection.commit()

        flash("You have successfully registered!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/student')
def student_dashboard():
    if 'loggedin' in session and session['role'] == 'student':
        return render_template('student.html', name=session['name'])
    return redirect(url_for('login'))

# @app.route('/admin')
# def admin_dashboard():
#     if 'loggedin' in session and session['role'] == 'admin':
#         cursor = mysql.connection.cursor()
#         cursor.execute("SELECT c.complaint_id,u.name,c.category,c.title,c.status FROM complaints c JOIN users u ON c.user_id=u.user_id")
#         complaints = cursor.fetchall()
#         return render_template('admin.html', complaints=complaints)
#     return redirect(url_for('login'))
@app.route('/admin')
def admin_dashboard():
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor()
        # ✅ Fetch description also
        cursor.execute("""
            SELECT c.complaint_id, u.name, c.category, c.title, c.description, c.status
            FROM complaints c 
            JOIN users u ON c.user_id=u.user_id
        """)
        complaints = cursor.fetchall()
        return render_template('admin.html', complaints=complaints)
    return redirect(url_for('login'))


@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    if 'loggedin' in session and session['role'] == 'student':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        cursor = mysql.connection.cursor()

        # ✅ Get max complaint_id
        cursor.execute("SELECT MAX(complaint_id) AS max_id FROM complaints")
        result = cursor.fetchone()
        next_id = 1 if result[0] is None else result[0] + 1  

        # ✅ Reset AUTO_INCREMENT
        cursor.execute("ALTER TABLE complaints AUTO_INCREMENT = %s", (next_id,))

        # ✅ Insert complaint
        cursor.execute("""
            INSERT INTO complaints (user_id, title, description, category, status) 
            VALUES (%s, %s, %s, %s, %s)
        """, (session['id'], title, description, category, "Pending"))
        
        mysql.connection.commit()
        return redirect(url_for('student_dashboard'))
    return redirect(url_for('login'))


@app.route('/my_complaints')
def my_complaints():
    if 'loggedin' not in session or session['role'] != 'student':
        return redirect(url_for('login'))

    user_id = session['id']  # get logged-in student's ID

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT complaint_id, title, description, category, status FROM complaints WHERE user_id=%s",
        (user_id,)
    )
    user_complaints = cursor.fetchall()
    cursor.close()

    return render_template("complaints.html", complaints=user_complaints)
    


@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    if 'loggedin' in session and session['role'] == 'admin':
        status = request.form['status']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE complaints SET status=%s WHERE complaint_id=%s",(status,id))
        mysql.connection.commit()
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
