import os
import sqlite3
import random
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_file
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

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/mod')
def mod():
    return render_template('mod.html')

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    counter = 0
    dot = -1
    if 'inputFile' not in request.files:
            flash('No selected file')
            return render_template('upload.html')
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
            return render_template('upload.html')
        lstring = len(Filename)
        Extension = Filename[(lstring - dot) * -1 :]
        Ecount = 7
        for i in ALLOWED_EXTENSIONS:
            if i != Extension:
                Ecount = Ecount - 1
        if Ecount == 0:
            flash('File type is not allow')
            return render_template('upload.html')
        Filename1 = str(random.randint(1,999999999))
        Filename2 = Filename1 + Extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], Filename2)) 
        cursor.execute("""INSERT INTO Exams (ExamID,CourseNum,Subj,ExamTitle,Semester,Extension)
        VALUES (?,?,?,?,?,?)""",(Filename1, Coursenum, Subject, Exam_title, Semester, Extension))
        connection.commit()
    return render_template('upload.html')

@app.route('/request', methods = ['POST', 'GET'])
def request_exam():
    return render_template('request.html')

@app.route('/modrequest', methods = ['POST', 'GET'])
def modrequest_exam():
    return render_template('modrequest.html')

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
    cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                      FROM Exams E
                      WHERE E.CourseNum = ? AND E.Subj = ? AND E.ExamTitle = ? AND E.Semester= ?""",(RCoursenum, RSubject, RExam_title, RSemester))
    Rexams = cursor.fetchall()
    return render_template('display.html', Rexams=Rexams)

@app.route('/return-file/<ID>', methods=['GET', 'POST'])
def return_file(ID):
    return send_file(os.path.join(app.root_path, 'downloads', ID))

@app.route('/displaymod', methods = ['POST', 'GET'])
def Mdisplay_exam():    
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
    cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                      FROM Exams E
                      WHERE E.CourseNum = ? AND E.Subj = ? AND E.ExamTitle = ? AND E.Semester= ?""",(RCoursenum, RSubject, RExam_title, RSemester))
    Rexams = cursor.fetchall()
    return render_template('Mdisplay.html', Rexams=Rexams)

@app.route('/ModifyB/<ID>', methods = ['POST', 'GET'])
def ModifyB(ID):
    print(ID)
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                      FROM Exams E
                      WHERE E.ExamID = %s"""%(ID))
    Rexams = cursor.fetchall()
    return render_template('ModifyB.html', Rexams=Rexams)

@app.route('/Modify/<ID>', methods = ['POST', 'GET'])
def Modify(ID):
    print(ID)
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                      FROM Exams E
                      WHERE E.ExamId = %s"""%(ID))
    Rexam = cursor.fetchone()
    CoursenumS = request.form['CourseNum']
    if(CoursenumS ==''):
        CoursenumS = Rexam["CourseNum"]
    Subject = request.form['Subject']
    if(Subject ==''):
        Subject = Rexam["Subj"]
    Exam_title = request.form['ExamTitle']
    if(Exam_title ==''):
        Exam_title = Rexam["ExamTitle"]
    Semester = request.form['Semester']
    if(Semester ==''):
        Semester = Rexam["Semester"]
    Extension = Rexam["Extension"]
    print('ASDASDASDHASJDHASKJ')
    print(Rexam["Subj"])
    cursor.execute("""DELETE FROM Exams
                    WHERE Exams.ExamID = %s""" % (ID))
    connection.commit()
    cursor.execute("""INSERT INTO Exams (ExamID,CourseNum,Subj,ExamTitle,Semester,Extension)
    VALUES (?,?,?,?,?,?)""",(ID, CoursenumS, Subject, Exam_title, Semester, Extension))
    connection.commit()
    cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                FROM Exams E
                WHERE E.CourseNum = ? AND E.Subj = ? AND E.ExamTitle = ? AND E.Semester= ?""",(CoursenumS, Subject, Exam_title, Semester))
    Rexams = cursor.fetchall()
    return render_template('Mdisplay.html', Rexams=Rexams)

@app.route('/delete/<ID>', methods = ['POST', 'GET'])
def delete(ID):
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                      FROM Exams E
                      WHERE E.ExamID = %s"""%(ID))
    Dexam = cursor.fetchone()
    cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                      FROM Exams E
                      WHERE E.CourseNum = ? AND E.Subj = ? AND E.ExamTitle = ? AND E.Semester= ? AND E.ExamID != ?""",(Dexam["CourseNum"], Dexam["Subj"], Dexam["Examtitle"], Dexam["Semester"], ID))
    Rexams = cursor.fetchall()
    cursor.execute("""DELETE FROM Exams
                      WHERE Exams.ExamID = %s"""%(ID))
    connection.commit()
    return render_template('Mdisplay.html', Rexams=Rexams)

app.run()