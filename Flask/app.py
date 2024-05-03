from flask import Flask, request, render_template, redirect, url_for, session
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

#index file
@app.route('/')
def index():
    if('loggedin') in session and 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')
    

@app.route('/catalog', methods=['Get','Post'])
def catalog():
    if(request.method == 'POST'):
        #insert code to add items to cart here
        print('YEA')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from product")
    data = cursor.fetchall()
    cursor.close()
    return render_template('catalog.html', Products=data)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        if 'loggedin' in session:  
            product_id = request.form.get('product_id')
            quantity = request.form.get('quantity')

            if product_id and quantity:
                # Check if the product exists in the product table
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
                product = cursor.fetchone()
                if product:
                    # Insert into orders table only if the product exists
                    cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (%s, %s, %s)",
                                   (session['id'], product_id, quantity))
                    mysql.connection.commit()
                    cursor.close()

                    msg = 'Product added to cart'
                    return redirect(url_for('cart'))
                else:
                    msg = 'Product does not exist'
            else:
                msg = 'Product ID and quantity are required'
        else:
            return redirect(url_for('login'))  # Redirect to login if not logged in
    
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        total_price = sum(product[4] for product in products)  # Accessing price from tuple by index
        cursor.close()
        
        return render_template('cart.html', products=products, total_price=total_price)
    else:
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

@app.route('/register', methods=['GET','POST'])
def register():
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