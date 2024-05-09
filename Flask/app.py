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
app.config['MYSQL_USER'] = 'cblaha1'
app.config['MYSQL_PASSWORD'] = 'Uq2pg8gG'
app.config['MYSQL_DB'] = 'cblaha1'

#Initialize MySQL
mysql = MySQL(app)



#index file
@app.route('/')
def index():
    if('loggedin') in session and 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')
    
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    if 'loggedin' not in session:
        return redirect('./login')
    if request.method == 'POST' and 'product_id' in request.form:
        # Get the product ID from the form data
        product_id = request.form.get('product_id')
        if product_id:
            # Check if the user is logged in
            if 'loggedin' in session:
                # Get the customer ID from the session
                customer_id = session['id']

                # Insert the item into the cart table
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE quantity = quantity + 1", (customer_id, product_id))
                mysql.connection.commit()
                cursor.close()
                flash('Product added to cart.', 'success')
            else:
                flash('Please log in to add products to the cart.', 'error')
        search_query = request.form.get('search')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM product WHERE product_name LIKE %s", ('%' + search_query + '%',))
        search_query = cursor.fetchall()
        cursor.close()
        return render_template('catalog.html', Products=search_query)
    elif request.method == 'POST' and 'search' in request.form:
        search = request.form['search']
        if search:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM product WHERE product_name LIKE %s", ('%' + search + '%',))
            search_query = cursor.fetchall()
            cursor.close()
            return render_template('catalog.html', Products=search_query)


    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM product")
    data = cursor.fetchall()
    cursor.close()
    return render_template('catalog.html', Products=data)

@app.route('/Profile', methods=['GET', 'POST'])
def Profile():
    msg=''
    if('loggedin') in session:
        current_customerID = session['id']
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            street = request.form['street']
            street_num = request.form['street_num']
            apt_num = request.form['apt_num']
            city = request.form['city']
            zip_code = request.form['zip_code']
            email=request.form['email']
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #cursor.execute('INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (current_username, first_name, last_name, email, street_num, street,
            #apt_num, city, zip_code, ))
            cursor.execute("""INSERT INTO customer (customer_ID, FirstName, LastName, email, street_number, street_name, apt_num, city, zip_code)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                              ON DUPLICATE KEY UPDATE
                              FirstName = VALUES(FirstName),
                              LastName = VALUES(LastName),
                              email = VALUES(email),
                              street_number = VALUES(street_number),
                              street_name = VALUES(street_name),
                              apt_num = VALUES(apt_num),
                              city = VALUES(city),
                              zip_code = VALUES(zip_code)""",
                           (current_customerID, first_name, last_name, email, street_num, street, apt_num, city, zip_code))
            mysql.connection.commit()
            msg = 'You have successfully changed your profile information'
            cursor.close()

        return render_template('profilein.html')
    else:
        return redirect(url_for('login'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Handle POST request to remove a product from the cart
        if 'loggedin' in session:
            remove = request.form['product_id']
            if remove:
                # Retrieve the customer ID from the session
                customer_id = session['id']
                # Delete the item from the cart table
                mysql.connection.cursor()
                cursor = mysql.connection.cursor()
                
                cursor.execute("DELETE FROM cart WHERE customer_id = %s AND product_id = %s", (customer_id, remove))
                mysql.connection.commit()
                flash('Product removed from cart.', 'success')
                cursor.close()
        else:
            flash('Please log in to remove products from the cart.', 'error')
        return redirect(url_for('cart'))

    # Handle GET request to display the cart
    if 'loggedin' in session:
        # Retrieve the customer ID from the session
        customer_id = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT p.*, c.quantity FROM product p INNER JOIN cart c ON p.product_ID = c.product_ID WHERE c.customer_ID = %s", (customer_id,))
        products = cursor.fetchall()
         
        sum = 0
        quantities=[]
        for item in products:
             product_id = item[0]  
             price = item[4]
             cursor.execute('SELECT quantity FROM cart WHERE product_ID = %s AND customer_ID = %s', (product_id, session['id']))
             quantity= cursor.fetchone()
             if quantity:
                sum+=quantity[0]*price
                quantities.append(quantity[0])

        cursor.close()

        return render_template('cart.html', products=products, total_price=sum ,total_quantity=quantities)
    else:
        flash('Please log in to view your cart.', 'error')
        return redirect(url_for('login'))


@app.route('/checkout', methods=['GET' , 'POST'])
def checkout():
    if request.method == 'POST' and 'cardnum' in request.form and 'Secode' in request.form and 'expdate' in request.form and 'loggedin' in session:
        cardnum = request.form['cardnum']
        Secode = request.form['Secode']
        expdate = request.form['expdate']
        #cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if not re.match(r'^\d{2}/\d{2}$', expdate):
            msg = 'Invalid expdate address!'
        elif not re.match(r'^\d{16}$', cardnum):
            msg = 'cardnum must contain only numbers!'
        elif not re.match(r'^\d{3}$', Secode):
            msg=" Invalid CVC code"
        elif not cardnum or not Secode or not expdate:
            msg = 'Please fill out the form!'
        else:
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO payment (customer_ID,card_number, security_code, expiration_date) VALUES (%s, %s, %s, %s)', (session['id'],cardnum, Secode, expdate,))
                mysql.connection.commit()
                cursor.close()
                msg = 'Payment successful!'
            except Exception as e:
                msg = 'Error: %s' % str(e)
                print("Error:", e)
        cursor.close()
        


    if 'loggedin' in session:
        # Retrieve the customer ID from the session
        customer_id = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT p.*, c.quantity FROM product p INNER JOIN cart c ON p.product_ID = c.product_ID WHERE c.customer_ID = %s", (customer_id,))
        products = cursor.fetchall()
         
        sum = 0
        quantitys=[]
        for item in products:
             product_id = item[0]  
             price = item[4]
             cursor.execute('SELECT quantity FROM cart WHERE product_ID = %s AND customer_ID = %s', (product_id, session['id']))
             quantity= cursor.fetchone()
             if quantity:
                sum+=quantity[0]*price
                quantitys.append(quantity[0])

        #Retrieve Payment Information for selected customer
        customer_id = session.get('id')

        #SQL query for retrieving payment information
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT card_number FROM payment WHERE customer_ID = %s", (customer_id,))
        existing_payments = cursor.fetchall()
        cursor.close()

        
        return render_template('checkout.html',total_price=sum, Products=products, quantity=quantitys)
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
  

@app.route('/payment', methods=['GET','POST'])
def payment():
    # Check if logged in 
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    # Retrieve customer_ID from session
    customer_id = session.get('id')

    # Display current payment info for the logged-in user
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT card_number FROM payment WHERE customer_ID = %s", (customer_id,))
    existing_payments = cursor.fetchall()
    cursor.close()

    # Form for adding payment info 
    if request.method == 'POST' and 'cardNum' in request.form and 'date' in request.form and 'cvc' in request.form and 'zip' in request.form:
        cardNum = request.form['cardNum']
        date = request.form['date']
        cvc = request.form['cvc']
        zip = request.form['zip']

        # Adding info to the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "INSERT INTO payment (customer_ID, card_number, expiration_date, security_code) VALUES (%s, %s, %s, %s)"
        values = (customer_id, cardNum, date, cvc)
        cursor.execute(sql, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('payment'))

    elif request.method == 'POST' and 'remove_payment' in request.form:
        cardNum = request.form['remove_payment']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "DELETE FROM payment WHERE customer_ID = %s AND card_number = %s"
        values = (customer_id, cardNum)
        cursor.execute(sql, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('payment'))

    return render_template('/payment.html', existing_payments=existing_payments)


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
            msg = 'You have successfully registered! Please sign in!'
        cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out registration form!'
    return render_template('/register.html', error=msg)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('id', None)
    session.pop('loggedin', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='localhost', port=5006)