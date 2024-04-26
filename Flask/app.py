from flask import Flask, request, render_template ,send_file
from flask_mysqldb import MySQL
from markupsafe import escape

app = Flask(__name__)

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
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from instructor")
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    #print(data)
    #return render_template('results.html', data=data)
    return render_template('index.html')

@app.route('/catalog')
def catalog():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from product")
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('catalog.html',Products=data)

@app.route('/payment')
def payment():
    return

#form
@app.route('/form')
def form():
    return render_template('form.html')
    
#result from form
@app.route('/search', methods = ['POST', 'GET'])
def search():
    if request.method == 'GET':
        return "Fill out the Search Form"
     
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        cursor = mysql.connection.cursor()
        if name:
            cursor.execute("SELECT * from instructor where name = %s",[name])
        if id:
            cursor.execute("SELECT * from instructor where ID = %s",[id])
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.close()
        print(data)
        #return f"Done!! Query Result is {data}"
        return render_template('results.html', data=data)

if __name__ == "__main__":
    app.run(host='localhost', port=5005)