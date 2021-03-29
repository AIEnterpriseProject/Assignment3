from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "flash message"
app.config['MYSQL_HOST'] = 'anisharora4.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'anisharora4'
app.config['MYSQL_PASSWORD'] = 'Asdfgh@123'
app.config['MYSQL_DB'] = 'anisharora4$crud'

mysql = MySQL(app)


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":

        flash("Data Inserted Successfully")
        fname = request.form['fname']
        lname = request.form['lname']
        dob = request.form['dob']
        amount = request.form['amount']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (first_name, last_name, dob, amount_due) VALUES (%s, %s, %s, %s)", (fname, lname, dob, amount))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        sid = request.form['sid']
        fname = request.form['fname']
        lname = request.form['lname']
        dob = request.form['dob']
        amount = request.form['amount']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET id=%s, first_name=%s, last_name=%s, dob=%s, amount_due=%s
               WHERE id=%s
            """, (sid, fname, lname, dob, amount, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['POST','GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("delete from students where id=%s",(id_data))
    flash("Data Deleted Successfully")
    mysql.connection.commit()
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
