import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask('DataBase')

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/studentinfo', methods=['POST'])
def studentinfo():
    name = request.form['Name']
    id = request.form['ID']

    print(name + id)
    return render_template('studentinfo.html', name=name)

app.run()