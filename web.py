import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER ='downloads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask('DataBase')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    file = request.files['inputFile']
    if file.filename == '':
            flash('No selected file')
    else:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return file.filename
app.run()