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

# This file create each individual webpage for our the projec by rendering the HTML that we 
# wrote in order to output the information we want

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/register', methods = ['POST', 'GET'])
def student():
    return render_template('register.html')

@app.route('/registered', methods = ['POST', 'GET'])
def registered():
    # Creating forms for user registration
    Accountid = request.form['un']
    First= request.form['fn']
    Middle = request.form['mn']
    Last = request.form['ln']
    Pass = request.form['pw']
    Email = request.form['em']
    University = request.form['uni']
    Location = request.form['loc']
    Stat = request.form['stat']

    # Error checking for empty user input 
    if Accountid == '' or First == '' or Last == '' or Pass == '' or Email == '':
        flash('First name, Last name, Password, or Email can not be empty')
        return render_template('register.html')
    if University !='' and Location == '':
        flash('Must provide a location for university')
        return render_template('register.html')

    # connect user inputs to database in order to create a new entry within the database
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT *
                      FROM Users U
                      WHERE  U.AccountID = '%s' """%(Accountid))
        no = cursor.fetchone()
        if no["AccountID"] != '':
            return redirect("/register")
    except:
        cursor.execute("""INSERT INTO Users (AccountID,Email,Fname,Lname,Mname)
        VALUES (?,?,?,?,?)""",(Accountid, Email, First, Last, Middle))
        connection.commit()
    try:
        cursor.execute("""SELECT U.UniName
                      FROM Uni U
                      WHERE  U.UniName = '%s' """%(University))
        ok = cursor.fetchone()
        if ok["UniName"] != '':
            print("Uni already in table")
    except:
        cursor.execute("""INSERT INTO Uni (Uniname,Loc)
        VALUES (?,?)""",(University,Location))
        connection.commit()
    cursor.execute("""INSERT INTO Attends (AccountID,Uniname,Stat)
    VALUES (?,?,?)""",(Accountid, University, Stat))
    # insert data into database
    connection.commit()
    # redirects to login when registration is successful
    return render_template('login.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/log', methods = ['POST', 'GET'])
def log():
    # create form for user to log in
    Accountid = request.form['UN']
    Password = request.form['PW']

    # ensure user is within the database to log in
    # also query the database to check if the user is a basic user or a mod
    # redirects the user to the correct upload page based on user type
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT U.AccountID
                      FROM Users U
                      WHERE  U.AccountID = '%s' """%(Accountid))
    us = cursor.fetchone()
    cursor.execute("""SELECT M.AccountID
                      FROM Mod1 M
                      WHERE M.AccountID = '%s' """%(Accountid))
    mo = cursor.fetchone()
    if Password == '':
        return redirect("login")
    try:
        if us['AccountID'] != "":
            return redirect("/upload")
    except:
        try:
            if mo['AccountID'] != "":
                return redirect("/mupload")
        except:
            flash('Username not found or Password is incorrect')
            return redirect("/login")

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    # connect to database in order to insert 
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    counter = 0
    dot = -1
    # form for user input
    # checks that each input
    if 'inputFile' not in request.files:
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
    ACCID = request.form['ACCID']
    # if informations are left blank, the users will be redirected back to upload
    # as these information cannot be blank, and the exam will not be added
    if (Coursenum == 0 or Subject == '' or Semester == ''or ACCID =='' or CoursenumS ==''):
        flash('Course Number, Subject, or Semester can not be blank')
        return redirect('/upload')
    # if all information are inputted, the exam will be added to the database
    # they will still be redirected back to the upload to submit another exam
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
    cursor.execute("""SELECT Base2.AccountID
                  FROM Base2 
                  WHERE  Base2.AccountID = '%s' """%(ACCID))
    no = cursor.fetchone()
    cursor.execute("""SELECT Base2.ExamsSubmitted
                  FROM Base2 
                  WHERE  Base2.AccountID = '%s' """%(ACCID))
    yo = cursor.fetchone()
    Start = 1
    print (no)
    try:
        cursor.execute("""INSERT INTO Base2 (AccountID,ExamsSubmitted)
        VALUES (?,?)""",(ACCID,Start))
        connection.commit()
    except:
        nub = yo[0]
        nub = nub + 1
        cursor.execute("""UPDATE Base2 
                          SET ExamsSubmitted = '%s'
                          Where  AccountID = '%s'"""%(nub,ACCID))
        connection.commit()
    return render_template('upload.html')

@app.route('/mupload', methods = ['POST', 'GET'])
# this fuction is almost identical to upload, but for mods. 
# this double fuctionality is to differentiate between the users
# and be able to direct mods to different areas that are not accessible 
# by normal users. Submittin exams and inserting is the same as upload
def mupload():  
    # connect to database
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    counter = 0
    dot = -1
    if 'inputFile' not in request.files:
            return render_template('mupload.html')
    file = request.files['inputFile']
    CoursenumS = request.form['CourseNum']
    if(CoursenumS ==''):
        Coursenum = 0
    else:
        Coursenum = int(CoursenumS)
    Subject = request.form['Subject']
    Exam_title = request.form['ExamTitle']
    Semester = request.form['Semester']
    ACCID = request.form['ACCID']
    if (Coursenum == 0 or Subject == '' or Semester == ''or ACCID =='' or CoursenumS ==''):
        flash('Course Number, Subject, or Semester can not be blank')
        return redirect('/mupload')
    else:
        Filename = secure_filename(file.filename)
        for i in Filename:
            if i == '.' :
                dot = counter
            else:
                counter = counter + 1 
        if(dot == -1):
            flash('There is not extenstion for this file')
            return render_template('mupload.html')
        lstring = len(Filename)
        Extension = Filename[(lstring - dot) * -1 :]
        Ecount = 7
        for i in ALLOWED_EXTENSIONS:
            if i != Extension:
                Ecount = Ecount - 1
        if Ecount == 0:
            flash('File type is not allow')
            return render_template('mupload.html')
        Filename1 = str(random.randint(1,999999999))
        Filename2 = Filename1 + Extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], Filename2)) 
        cursor.execute("""INSERT INTO Exams (ExamID,CourseNum,Subj,ExamTitle,Semester,Extension)
        VALUES (?,?,?,?,?,?)""",(Filename1, Coursenum, Subject, Exam_title, Semester, Extension))
        connection.commit()
    cursor.execute("""SELECT Base2.AccountID
                  FROM Base2 
                  WHERE  Base2.AccountID = '%s' """%(ACCID))
    no = cursor.fetchone()
    cursor.execute("""SELECT Base2.ExamsSubmitted
                  FROM Base2 
                  WHERE  Base2.AccountID = '%s' """%(ACCID))
    yo = cursor.fetchone()
    Start = 1
    print (no)
    try:
        cursor.execute("""INSERT INTO Base2 (AccountID,ExamsSubmitted)
        VALUES (?,?)""",(ACCID,Start))
        connection.commit()
    except:
        print("ASDJASDJASDJHASJH")
        nub = yo[0]
        nub = nub + 1
        cursor.execute("""UPDATE Base2 
                          SET ExamsSubmitted = '%s'
                          WHERE  AccountID = '%s'"""%(nub,ACCID))
        connection.commit()
    return render_template('mupload.html')

# these two request functions let users input information about exams 
@app.route('/request', methods = ['POST', 'GET'])
def request_exam():
    return render_template('request.html')

@app.route('/modrequest', methods = ['POST', 'GET'])
def modrequest_exam():
    return render_template('modrequest.html')

@app.route('/display', methods = ['POST', 'GET'])
# this is the display for normal users
def display_exam():
    # connect to database
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # get the information the users are searching for via the form
    # from request.html
    RCoursenumS = request.form['RCourseNum']
    if(RCoursenumS ==''):
        RCoursenum = 0
    else:
        RCoursenum = int(RCoursenumS)
    RSubject = request.form['RSubject']
    RExam_title = request.form['RExamTitle']
    RSemester = request.form['RSemester']
    # query for what the user is looking for within the database
    if RSubject == '' and RExam_title == '' and RSemester == '' and RCoursenum == 0:
        cursor.execute("""SELECT *
                          FROM Exams """)
        Rexams = cursor.fetchall()
    elif RSubject == '' and RExam_title != '' and RSemester != '' and RCoursenum != 0:
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = ?  AND E.ExamTitle = ? AND E.Semester = ?""",(RCoursenum, RExam_title, RSemester))
        Rexams = cursor.fetchall()
    elif RSubject != '' and RExam_title == '' and RSemester == '' and RCoursenum == 0:
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.Subj= '%s' """%(RSubject))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RExam_title == '' and RSemester == ''and RCoursenum != 0:
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = '%s' """%(RCoursenum))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RExam_title == '' and RCoursenum != 0 and RSemester != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = ?  AND E.Semester = ?""",(RCoursenum, RSemester))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RExam_title == '' and RCoursenum == 0 and RSemester != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.Semester = '%s'"""%(RSemester))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RCoursenum == 0 and RSemester != '' and RExam_title != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.ExamTitle = ? AND E.Semester = ?""",(RExam_title, RSemester))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RCoursenum == 0 and RSemester == '' and RExam_title != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.ExamTitle = '%s' """%(RExam_title))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RSemester == '' and RCoursenum != 0 and RExam_title != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = ? AND E.ExamTitle = ? """,(RCoursenum,RExam_title))
        Rexams = cursor.fetchall()
    elif RSemester == '' and RCoursenum != 0 and RSubject != '' and RExam_title != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = ? AND E.Subj = ? AND E.ExamTitle = ? """,(RCoursenum, RSubject, RExam_title))
        Rexams = cursor.fetchall()
    elif RSemester == '' and RCoursenum == 0 and RSubject != '' and RExam_title != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.Subj = ? AND E.ExamTitle = ? """,(RSubject, RExam_title))
        Rexams = cursor.fetchall()
    elif RSemester == '' and RExam_title == '' and RCoursenum != 0 and RSubject != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = ? AND E.Subj = ? AND E.ExamTitle = ? AND E.Semester = ?""",(RCoursenum, RSubject))
        Rexams = cursor.fetchall()
    elif RExam_title == '' and RCoursenum == 0 and RSubject != '' and RSemester != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.Subj = ?  AND E.Semester = ?""",(RSubject, RSemester))
        Rexams = cursor.fetchall()
    elif RCoursenum == 0 and RSemester != '' and RSubject != '' and RCoursenum != 0: 
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.Subj = ? AND E.ExamTitle = ? AND E.Semester = ?""",(RSubject, RExam_title, RSemester))
        Rexams = cursor.fetchall()
    else:
        cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                          FROM Exams E
                          WHERE E.CourseNum = ? AND E.Subj = ? AND E.ExamTitle = ? AND E.Semester = ?""",(RCoursenum, RSubject, RExam_title, RSemester))
        Rexams = cursor.fetchall()
    return render_template('display.html', Rexams=Rexams)

@app.route('/return-file/<ID>', methods=['GET', 'POST'])
def return_file(ID):
    return send_file(os.path.join(app.root_path, 'downloads', ID))

@app.route('/displaymod', methods = ['POST', 'GET'])
# identical to /display
# however, the mod will be able to modify or delete exams from the database
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
    if RSubject == '' and RExam_title == '' and RSemester == '' and RCoursenum == 0:
        cursor.execute("""SELECT *
                          FROM Exams """)
        Rexams = cursor.fetchall()
    elif RSubject == '' and RExam_title != '' and RSemester != '' and RCoursenum != 0:
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = ?  AND E.ExamTitle = ? AND E.Semester = ?""",(RCoursenum, RExam_title, RSemester))
        Rexams = cursor.fetchall()
    elif RSubject != '' and RExam_title == '' and RSemester == '' and RCoursenum == 0:
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.Subj= '%s' """%(RSubject))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RExam_title == '' and RSemester == ''and RCoursenum != 0:
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = '%s' """%(RCoursenum))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RExam_title == '' and RCoursenum != 0 and RSemester != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = ?  AND E.Semester = ?""",(RCoursenum, RSemester))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RExam_title == '' and RCoursenum == 0 and RSemester != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.Semester = '%s'"""%(RSemester))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RCoursenum == 0 and RSemester != '' and RExam_title != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.ExamTitle = ? AND E.Semester = ?""",(RExam_title, RSemester))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RCoursenum == 0 and RSemester == '' and RExam_title != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.ExamTitle = '%s' """%(RExam_title))
        Rexams = cursor.fetchall()
    elif RSubject == '' and RSemester == '' and RCoursenum != 0 and RExam_title != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = ? AND E.ExamTitle = ? """,(RCoursenum,RExam_title))
        Rexams = cursor.fetchall()
    elif RSemester == '' and RCoursenum != 0 and RSubject != '' and RExam_title != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = ? AND E.Subj = ? AND E.ExamTitle = ? """,(RCoursenum, RSubject, RExam_title))
        Rexams = cursor.fetchall()
    elif RSemester == '' and RCoursenum == 0 and RSubject != '' and RExam_title != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.Subj = ? AND E.ExamTitle = ? """,(RSubject, RExam_title))
        Rexams = cursor.fetchall()
    elif RSemester == '' and RExam_title == '' and RCoursenum != 0 and RSubject != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.CourseNum = ? AND E.Subj = ? AND E.ExamTitle = ? AND E.Semester = ?""",(RCoursenum, RSubject))
        Rexams = cursor.fetchall()
    elif RExam_title == '' and RCoursenum == 0 and RSubject != '' and RSemester != '':
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.Subj = ?  AND E.Semester = ?""",(RSubject, RSemester))
        Rexams = cursor.fetchall()
    elif RCoursenum == 0 and RSemester != '' and RSubject != '' and RCoursenum != 0: 
        cursor.execute("""SELECT *
                          FROM Exams E
                          WHERE E.Subj = ? AND E.ExamTitle = ? AND E.Semester = ?""",(RSubject, RExam_title, RSemester))
        Rexams = cursor.fetchall()
    else:
        cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                          FROM Exams E
                          WHERE E.CourseNum = ? AND E.Subj = ? AND E.ExamTitle = ? AND E.Semester = ?""",(RCoursenum, RSubject, RExam_title, RSemester))
        Rexams = cursor.fetchall()
    return render_template('Mdisplay.html', Rexams=Rexams)

@app.route('/ModifyB/<ID>', methods = ['POST', 'GET'])
# if mods decide to modify an exam they will be asked for new inputs
def ModifyB(ID):
    # this will display the exam the moderator decide to modify and allow them to input new data
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                      FROM Exams E
                      WHERE E.ExamID = %s"""%(ID))
    Rexams = cursor.fetchall()
    return render_template('ModifyB.html', Rexams=Rexams)

@app.route('/Modify/<ID>', methods = ['POST', 'GET'])
# once mods entered new data this will execute the chagnes
def Modify(ID):
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                      FROM Exams E
                      WHERE E.ExamId = %s"""%(ID))
    Rexam = cursor.fetchone()
    CoursenumS = request.form['CourseNum']
    # check each new input and update the database
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
    cursor.execute("""DELETE FROM Exams
                    WHERE Exams.ExamID = %s""" % (ID))
    connection.commit()
    cursor.execute("""INSERT INTO Exams (ExamID,CourseNum,Subj,ExamTitle,Semester,Extension)
    VALUES (?,?,?,?,?,?)""",(ID, CoursenumS, Subject, Exam_title, Semester, Extension))
    connection.commit()
    cursor.execute("""SELECT E.ExamID, E.CourseNum, E.Subj, E.ExamTitle, E.Semester, E.Extension
                FROM Exams E""")
    Rexams = cursor.fetchall()
    # redirect to view the updated changes
    return render_template('Mdisplay.html', Rexams=Rexams)

@app.route('/delete/<ID>', methods = ['POST', 'GET'])
# if mods want to delete an exam, they will select it and 
# the page will redirect to a page of all exams which will 
# no longer have the one they just deleted
def delete(ID):
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT *
                      FROM Exams E""")
    Rexams = cursor.fetchall()
    cursor.execute("""DELETE FROM Exams
                      WHERE Exams.ExamID = '%s'"""%(ID))
    connection.commit() 
    cursor.execute("""SELECT *
                      FROM Exams E""")
    Rexams = cursor.fetchall()

    return render_template('Mdisplay.html', Rexams=Rexams)

@app.route('/NumbersExam', methods = ['POST', 'GET'])
# let users view how many exams each users have submitted
def Numbers_of_Exam():
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT *
                      FROM Base2 """)
    Exams = cursor.fetchall()
    return render_template("NoExams.html", Exams=Exams)
app.run()