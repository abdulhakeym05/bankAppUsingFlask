from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import bcrypt

# Setup
app = Flask(__name__)
app.secret_key = "hakeym05"  # Add your secret key for session management

# SQLite connection
conn = sqlite3.connect('bankdata.db')
cursor = conn.cursor()

# Function to get a database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('bankdata.db')
    return g.db

# Function to close the database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# -----------------------------

# Routes pages

@app.route('/')
@app.route('/home')
def home():
    return render_template('landing.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/Board')
def dashboard():
    return render_template('Dashboard.html')

@app.route('/register')
def register():
    return render_template('form.html')

@app.route('/signin')
def signin():
    return render_template('login.html')

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ---------
# login form
@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password'].encode('utf-8')  # Encode password as a byte string
    
    # Query to get the data from the database and compare with the login page
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers WHERE name=?", (name,))
    user = cursor.fetchone()

    # Check if the user exists
    if user:
        hashed_password = user[5]  # Assuming the hashed password is in the sixth column (index 5) of the SELECT statement.
        if bcrypt.checkpw(password, hashed_password.encode('utf-8')):
            # Password is correct, user is authenticated
            return render_template('userDashboard.html')
        else:
            # Incorrect password
            
            # Check the number of login attempts for the user and update the count
            session['login_attempts'] = session.get('login_attempts', 0) + 1

            if session['login_attempts'] >= 3:
                # If the user has exceeded the maximum login attempts, display a warning
                return render_template('login.html', message='Maximum login attempts exceeded. Please try again later.')

            # If the password is incorrect but the number of login attempts is less than 3, show an error message
            return render_template('login.html', message='Incorrect password. Please try again.')
    else:
        # User does not exist
        return render_template('login.html', message='User does not exist.')

    # Close the database connection (if you have a function to close the connection)
    close_db(user)


# -------------------------------------------
## Register page or form
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone_number = request.form['phone_number']
        password = request.form.get('password')
        confirm_password = request.form.get('Confirm_password')
        email = request.form['email']

        # Registration Validations:

        # 1 Username validation: Ensure the username is not empty.
        if not name:
            return render_template('form.html', message='Username cannot be empty.')

        # 2 Check if the username already exists in the database.
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM customers WHERE name=?", (name,))
        existing_user = cursor.fetchone()
        if existing_user:
            return render_template('form.html', message='Username already exists.')

        # Password validation:
        # 1 Verify that the password meets complexity requirements (e.g., minimum length, presence of special characters, etc.).
        if len(password) < 8:
            return render_template('form.html', message='Password must be at least 8 characters long.')

        # 2 Compare the password and confirm password fields to ensure they match.
        #if password != confirm_password:
        #    return render_template('form.html', message='Passwords do not match.')

        # Password hashing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Generate a valid salt for hashing

        # Insert user data into the database
        cursor.execute("INSERT INTO customers (name, address, phone_number, password, email) VALUES (?, ?, ?, ?, ?)",
                       (name, address, phone_number, hashed_password.decode('utf-8'), email))  # Decode the hashed password before insertion
        db.commit()

        return redirect(url_for('signin'))

    return render_template('form.html')


if __name__ == "__main__":
    app.run(debug=True)


'''
#--------------------------------Naveeen's Add Data----------------------------------------
@app.route('/form2', methods=['GET', 'POST'])
def form2():
    if request.method == 'POST':
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        price = request.form['price']
        Quantity = request.form['Quantity']

        # Use a context manager to handle the connection and ensure proper closing
        with sqlite3.connect('bankdata.db') as conne:
            z = conne.cursor()
            z.execute("INSERT INTO data (product_id, product_name, price, Quantity) VALUES (?, ?, ?, ?)",
                      (product_id, product_name, price, Quantity))

        return render_template('data.html')

    return render_template('register.html')
'''

