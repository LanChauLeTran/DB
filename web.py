import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask('DataBase')

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Welcome! <a href='/logout'>Logout</a>"

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
    
@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/studentinfo', methods=['POST'])
def studentinfo():
    name = request.form['Name']
    id = request.form['ID']

    print(name + id)
    return render_template('studentinfo.html', name=name)

app.run()