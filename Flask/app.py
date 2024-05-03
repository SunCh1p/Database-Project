from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

#Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'aalluhai'
app.config['MYSQL_PASSWORD'] = 'EGj62ysf'
app.config['MYSQL_DB'] = 'aalluhai'

#Initialize MySQL
mysql = MySQL(app)

@app.before_request
def clear_session():
    session.clear()

#index file
@app.route('/')
def index():
    if('loggedin') in session and 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')
    
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    if request.method == 'POST':
        # Get the product ID from the form data
        product_id = request.form.get('product_id')
        if product_id:
            # Check if the product is already in the cart
            if 'cart' not in session:
                session['cart'] = {}  # Initialize cart if not already present in session
            cart = session['cart']

            # Update cart: Increment quantity if product is already in the cart, otherwise add it
            cart[product_id] = cart.get(product_id, 0) + 1
            session['cart'] = cart
            print('Product added to cart:', product_id)

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM product")
    data = cursor.fetchall()
    cursor.close()
    return render_template('catalog.html', Products=data)


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        # Handle POST request to remove a product from the cart
        if 'loggedin' in session:
            product_id_to_remove = request.form.get('remove_product_id')
            if product_id_to_remove:
                # Retrieve cart data from session
                cart = session.get('cart', {})
                # Remove the product from the cart if it exists
                if product_id_to_remove in cart:
                    del cart[product_id_to_remove]
                    session['cart'] = cart
                    flash('Product removed from cart.', 'success')
                else:
                    flash('Product not found in cart.', 'error')
            else:
                flash('Product ID to remove not provided.', 'error')
        else:
            flash('Please log in to remove products from the cart.', 'error')
        return redirect(url_for('cart'))

    # Handle GET request to display the cart
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        cursor.close()
        
        # Retrieve cart data from session
        cart = session.get('cart', {})
        
        # Convert product IDs to strings in the cart
        cart_str = {str(product_id): quantity for product_id, quantity in cart.items()}
        
        # Calculate total price of items in the cart
        total_price = sum(product[4] * cart_str.get(str(product[0]), 0) for product in products)  # Accessing price from tuple by index
        
        return render_template('cart.html', products=products, cart=cart_str, total_price=total_price)
    else:
        flash('Please log in to view your cart.', 'error')
        return redirect(url_for('login'))





@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (escape(username),))
        account = cursor.fetchone()
        cursor.close()
        if account and check_password_hash(account['password'],password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect('/')
        else:
            return render_template('/login.html', error = 'Incorrect username/Password!')
    return render_template('/login.html')
  

@app.route('/payment')
def payment():
    return

@app.route('/register', methods=['GET','POST'])
def register():
    if('loggedin') in session and 'username' in session:
        return redirect(url_for('index'))

    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashed_password = generate_password_hash(password)
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg='Account with that username already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, hashed_password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
        cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out registration form!'
    return render_template('/register.html', error=msg)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('id', None)
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='localhost', port=5006)