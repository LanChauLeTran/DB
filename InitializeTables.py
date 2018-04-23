import sqlite3
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute('CREATE TABLE Exams('###################################
        'ExamID         char(9)         PRIMARY KEY,'
        'CourseNum      int             NOT NULL   ,'
        'Subj           char(20)        NOT NULL   ,'
        'ExamTitle      char(50)                   ,'
        'Semester       char(10)        NOT NULL    '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE Users('###################################
        'AccountID      char(9)         PRIMARY KEY,'
        'Email          char(50)                   ,'
        'Fname          char(20)                   ,'
        'Lname          char(20)                   ,'
        'Mname          char(1)                     '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE Base1('###################################
        'AccountID  char(9)  PRIMARY KEY  REFERENCES Users(AccountID),'
        'Datejoined date                                              '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE Base2('###################################
        'AccountID      char(9)         REFERENCES Users(AccountiD),'
        'ExamsSubmitted char(9)         REFERENCES EXAMS(ExamID    ,'
        'PRIMARY KEY(AccountiD, ExamsSubmitted)                     '
        ');')
conection.commit()#####################################################

cursor.execute('CREATE TABLE Mod1('####################################
        'AccountID      char(9)         REFERENCES Users(AccountID),'
        'DateVerified   date                                       ,'
        'ModID          char(9)                                    ,'
        'PRIMARY KEY(AccountID, ModID)                              '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE Mod2('####################################
        'AccountID      char(9)         REFERENCES Users(AccountID),'
        'ExamsReviewed  char(9)         REFERENCES Exams(ExamID)   ,'
        'ModID          char(9)         REFERENCES Mod1(ModID)     ,'
        'PRIMARY KEY(AccountID, ExamsReviewd, ModID)                '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE Mod3('####################################
        'AccountID      char(9)         REFERENCES Users(AccountID),'
        'PendingReviews char(9)         REFERENCES Exams(ExamID)   ,'
        'ModID          char(9)         REFERENCES Mod1(ModID)     ,'
        'PRIMARY KEY(AccountID, PendingReviews, ModID)              '
        ');')
conection.commit()#####################################################

cursor.execute('CREATE TABLE Uni('#####################################
        'UniName char(50)       PRIMARY KEY,'
        'Loc     char(50)                   '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE Attends('#################################
        'AccountID      char(9)         REFERENCES Users(AccountID),'
        'UniName        char(50)        REFERENCES Uni(UniName)    ,'
        'Stat           char(20)                                   ,'
        'PRIMARY KEY(AccountID, UniName)                            '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE Instructors('#############################
        'Fname          char(20)                                ,'
        'Lname          char(20)                                ,'
        'UniName        char(20)        REFERENCES Uni(UniName) ,'
        'ExamID         char(9)         REFERENCES Exams(ExamID),'
        'PRIMARY KEY(Fname, Lname, UniName, ExamID)              '
        ');')
connection.commit()####################################################


#################### START OF INSERTING DATA ##########################

### Insert into Exams ###
cursor.execute('INSERT INTO Exams VALUES ("123456789", 1222 , "Math", "Calc 2 Exam 1", "Spring 2016")')  
connection.commit()

