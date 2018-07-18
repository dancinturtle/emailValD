from flask import Flask, request, redirect, render_template, flash, session
import re
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "almondMilkIsNotThatBadIhaveBeenConvinced"
mysql = connectToMySQL('emailVal')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process", methods=["POST"])
def process():
    emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not emailRegex.match(request.form['email']):
        flash(request.form['email'], 'bademail')
        # session['bademail'] = request.form['email']
        flash("Email must be valid!", 'error')
        return redirect('/')
    query = "SELECT id FROM users WHERE email = %(email)s;"
    data = {'email': request.form['email']}
    found = mysql.query_db(query, data)
    print("how many?", len(found))
    if found:
        flash("This email is already taken!", 'error')
        flash(request.form['email'], 'bademail')
        return redirect('/')
    flash(f"The email address you entered ({request.form['email']}) is a VALID email address! Thank you!")
    query = "INSERT INTO users (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
    data = {"email" : request.form['email']}
    result = mysql.query_db(query, data)
    if 'bademail' in session:
        session.pop('bademail')
    return redirect('/success')

@app.route('/success')
def success():
    query = "SELECT id, email, created_at FROM users;"
    emails = mysql.query_db(query)
    return render_template('success.html', emails = emails)

@app.route('/delete/<id>')
def delete(id):
    query = "DELETE FROM users WHERE id = %(id)s;"
    data = {"id": id}
    result = mysql.query_db(query, data)
    print('result from deleting', result)
    return redirect('/success')

if __name__ == "__main__":
    app.run(debug=True)
