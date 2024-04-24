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
    print(data)
    return f"Done!! Query Result is {data}"

if __name__ == "__main__":
    app.run(host='localhost', port=5005)