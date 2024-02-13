from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskappcrudapplication'

# Initialize MySQL
mysql = MySQL(app)


@app.route('/')
def index():
    # Retrieve all students from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    return render_template('index.html', students=students)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Insert data into database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        cur.close()

        # Redirect to index page after insertion
        return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        # Fetch student data from database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students WHERE id = %s", (id,))
        student = cur.fetchone()
        cur.close()

        # Render edit form with student data
        return render_template('edit.html', student=student)

    elif request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Update data in database
        cur = mysql.connection.cursor()
        cur.execute("UPDATE students SET name=%s, email=%s, phone=%s WHERE id=%s", (name, email, phone, id))
        mysql.connection.commit()
        cur.close()

        # Redirect to index page after update
        return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST':
        # Delete data from database
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()

        # Redirect to index page after deletion
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
