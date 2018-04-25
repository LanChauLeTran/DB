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
        'ExamsSubmitted char(9)         REFERENCES EXAMS(ExamID)    ,'
        'PRIMARY KEY(AccountiD, ExamsSubmitted)                     '
        ');')
connection.commit()#####################################################

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
connection.commit()#####################################################

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

cursor.execute('INSERT INTO Exams VALUES ("000000000", 1120, "English", "Eng 1 Midterms", "Fall 2017")')
connection.commit()

cursor.execute('INSERT INTO Exams VALUES ("987654321", 2135, "Physics, "Physics 2 Exam 2", "Spring 2018")')
connection.commit()
###########################################################################################################
cursor.execute('INSERT INTO Users VALUES ("111111111", "Johnny@gmail.com", "Johnathan", "Smith", NULL)')
connection.commit()

cursor.execute('INSERT INTO Users VALUES ("222222222", "Jeff@gmail.com", "Jeff", "Bezos", "J")')
connection.commit()

cursor.execute('INSERT INTO Users VALUES ("333333333", "Anne@gmail.com", "Anne", "Winters", "O")')
connection.commit()
###########################################################################################################
cursor.execute('INSERT INTO Base1 VALUES ("111111111", 2018-04-20)')
connection.commit()

cursor.execute('INSERT INTO Base1 VALUES ("222222222", 2018-08-05)')
connection.commit()

cursor.execute('INSERT INTO Base1 VALUES ("333333333", 2018-06-09)')
connection.commit()
###########################################################################################################
cursor.execute('INSERT INTO Base2 VALUES ("111111111", "000000000")')
connection.commit()

cursor.execute('INSERT INTO Base2 VALUES ("111111111", "123456789")')
connection.commit()

cursor.execute('INSERT INTO Base2 VALUES ("222222222", "987654321")')
connection.commit()
###########################################################################################################
cursor.execute('INSERT INTO Mod1 VALUES ("123123123", 2018-01-01, "101010101")')
connection.commit()

cursor.execute('INSERT INTO Mod1 VALUES ("456456456", 2018-02-01, "202020202")')
connection.commit()

cursor.execute('INSERT INTO Mod1 VALUES ("789789789", 2018-06-02, "303030303")')
connection.commit()
###########################################################################################################
cursor.execute('INSERT INTO Mod2 VALUES ("123123123", 8, "101010101")')
connection.commit()

cursor.execute('INSERT INTO Mod2 VALUES ("456456456", 71, "202020202")')
connection.commit()

cursor.execute('INSERT INTO Mod2 VALUES ("789789789", 54, "303030303")')
connection.commit()
###########################################################################################################
cursor.execute('INSERT INTO Mod3 VALUES ("123123123", 512, "101010101")')
connection.commit()

cursor.execute('INSERT INTO Mod3 VALUES ("456456456", 1, "202020202")')
connection.commit()

cursor.execute('INSERT INTO Mod3 VALUES ("789789789", 21, "303030303")')
connection.commit()
###########################################################################################################
cursor.execute('INSERT INTO Uni VALUES ("MS&T", "Rolla")')
connection.commit()

cursor.execute('INSERT INTO Uni VALUES ("Mizzou", "Columiba")')
connection.commit()

cursor.execute('INSERT INTO Uni VALUES ("UMSL", "St. Louis")')
connection.commit()
###########################################################################################################
cursor.execute('INSERT INTO Attends VALUES ("111111111", "MS&T", "Senior")')
connection.commit()

cursor.execute('INSERT INTO Attends VALUES ("22222222","Mizzou", "Junior")')
connection.commit()

cursor.execute('INSERT INTO Attends VALUES ("333333333","UMSL", "Freshman")')
connection.commit()
###########################################################################################################
cursor.execute('INSERT INTO Instructors VALUES ("Kim", "Possible" , "MS&T", "111111111")')
connection.commit()

cursor.execute('INSERT INTO Instructors VALUES ("Timmy", "Turner" ,"Mizzou", "222222222")')
connection.commit()

cursor.execute('INSERT INTO Instructors VALUES ("Scooby", "Doo", "UMSL", "333333333")')
connection.commit()