import os
import sqlite3
import random
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug.utils import secure_filename
from os import path

UPLOAD_FOLDER ='downloads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'])
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
    Coursenum = request.form['CourseNum']
    Subject = request.form['Subject']
    Exam_title = request.form['ExamTitle']
    Semester = request.form['Semester']
    if (Coursenum == '' or Subject == '' or Semester == ''):
        flash('Course Number, Subject, or Semester can not be blank')
    elif (file.filename == ''):
        flash('No selected file')
    else:
        filename = secure_filename(file.filename)
        if(filename[-4] == "."):
            extension = filename[-4:]
        else: 
            extension = filename[-5:]
        filename = str(random.randint(1,999999999)) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
        #cursor.execute('INSERT INTO Exams VALUES (Filename, Coursenum, Subject, Exam_title, Semester)')
        #connection.commit()
    return render_template('studentinfo.html')
app.run()
