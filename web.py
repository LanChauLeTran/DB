import os
import sqlite3
import random
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug.utils import secure_filename
from os import path

UPLOAD_FOLDER ='downloads'
ALLOWED_EXTENSIONS = set(['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.docx'])
app = Flask('DataBase')
app.secret_key = 'secret'
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
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    counter = 0
    dot = -1
    if 'inputFile' not in request.files:
            flash('No selected file')
            return render_template('studentinfo.html')
    file = request.files['inputFile']
    CoursenumS = request.form['CourseNum']
    if(CoursenumS ==''):
        Coursenum = 0
    else:
        Coursenum = int(CoursenumS)
    Subject = request.form['Subject']
    Exam_title = request.form['ExamTitle']
    Semester = request.form['Semester']
 
    if (Coursenum == 0 or Subject == '' or Semester == ''):
        flash('Course Number, Subject, or Semester can not be blank')
    else:
        Filename = secure_filename(file.filename)
        for i in Filename:
            if i == '.' :
                dot = counter
            else:
                counter = counter + 1 
        if(dot == -1):
            flash('There is not extenstion for this file')
            return render_template('studentinfo.html')
        lstring = len(Filename)
        extension = Filename[(lstring - dot) * -1 :]
        Ecount = 7
        for i in ALLOWED_EXTENSIONS:
            if i != extension:
                Ecount = Ecount - 1
        if Ecount == 0:
            flash('File type is not allow')
            return render_template('studentinfo.html')
        Filename1 = str(random.randint(1,999999999))
        Filename2 = Filename1 + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], Filename2)) 
        cursor.execute("""INSERT INTO Exams (ExamID,CourseNum,Subj,ExamTitle,Semester)
        VALUES (?,?,?,?,?)""",(Filename1, Coursenum, Subject, Exam_title, Semester))
        connection.commit()
    return render_template('studentinfo.html')

@app.route('/request', methods = ['POST', 'GET'])
def request_exam():
    return render_template('request.html')

@app.route('/display', methods = ['POST', 'GET'])
def display_exam():
    
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    RCoursenumS = request.form['RCourseNum']
    if(RCoursenumS ==''):
        RCoursenum = 0
    else:
        RCoursenum = int(RCoursenumS)
    RSubject = request.form['RSubject']
    RExam_title = request.form['RExamTitle']
    RSemester = request.form['RSemester']
    print (RCoursenum, RSubject, RExam_title, RSemester)
    cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester
                      FROM Exams E
                      WHERE E.CourseNum = ? AND E.Subj = ? AND E.ExamTitle = ? AND E.Semester= ?""",(RCoursenum, RSubject, RExam_title, RSemester))
    Rexams = cursor.fetchall()
    return render_template('display.html', Rexams=Rexams)



app.run()
