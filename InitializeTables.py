import sqlite3
connection = sqlite3.connect("data.db")
cursor = connection.cursor()


cursor.execute('CREATE TABLE IF NOT EXISTS [Exams]('###################################
        'ExamID         varchar         PRIMARY KEY,'
        'CourseNum      int             NOT NULL   ,'
        'Subj           varchar        NOT NULL   ,'
        'ExamTitle      varchar        NOT NULL   ,'
        'Semester       varchar       NOT NULL    ,'
        'Extension     varchar       NOT NULL'
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE IF NOT EXISTS [Users]('###################################
        'AccountID      varchar         PRIMARY KEY,'
        'Email          varchar                  ,'
        'Fname          varchar                  ,'
        'Lname          varchar                  ,'
        'Mname          varchar                     '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE IF NOT EXISTS [Base1]('###################################
        'AccountID  varchar  PRIMARY KEY  REFERENCES Users(AccountID),'
        'Datejoined date                                              '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE IF NOT EXISTS [Base2]('###################################
        'AccountID      varchar         REFERENCES Users(AccountiD),'
        'ExamsSubmitted int         REFERENCES EXAMS(ExamID)    ,'
        'PRIMARY KEY(AccountiD, ExamsSubmitted)                     '
        ');')
connection.commit()#####################################################

cursor.execute('CREATE TABLE IF NOT EXISTS [Mod1]('####################################
        'AccountID      varchar        REFERENCES Users(AccountID),'
        'DateVerified   date                                       ,'
        'ModID          varchar                                    ,'
        'PRIMARY KEY(AccountID, ModID)                              '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE IF NOT EXISTS [Mod2]('####################################
        'AccountID      varchar         REFERENCES Users(AccountID),'
        'ExamsReviewed  varchar         REFERENCES Exams(ExamID)   ,'
        'ModID          varchar         REFERENCES Mod1(ModID)     ,'
        'PRIMARY KEY(AccountID, ExamsReviewed, ModID)                '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE IF NOT EXISTS [Mod3]('####################################
        'AccountID      varchar         REFERENCES Users(AccountID),'
        'PendingReviews varchar         REFERENCES Exams(ExamID)   ,'
        'ModID          varchar         REFERENCES Mod1(ModID)     ,'
        'PRIMARY KEY(AccountID, PendingReviews, ModID)              '
        ');')
connection.commit()#####################################################

cursor.execute('CREATE TABLE IF NOT EXISTS [Uni]('#####################################
        'UniName varchar       PRIMARY KEY,'
        'Loc     varchar                   '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE IF NOT EXISTS [Attends]('#################################
        'AccountID      varchar        REFERENCES Users(AccountID),'
        'UniName        varchar        REFERENCES Uni(UniName)    ,'
        'Stat           varchar                                   ,'
        'PRIMARY KEY(AccountID, UniName)                            '
        ');')
connection.commit()####################################################

cursor.execute('CREATE TABLE IF NOT EXISTS [Instructors]('#############################
        'Fname          varchar                                ,'
        'Lname          varchar                                ,'
        'UniName        varchar        REFERENCES Uni(UniName) ,'
        'ExamID         varchar        REFERENCES Exams(ExamID),'
        'PRIMARY KEY(Fname, Lname, UniName, ExamID)              '
        ');')
connection.commit()####################################################


#################### START OF INSERTING DATA ##########################

### Insert into Exams ##### 
cursor.execute('INSERT INTO Exams VALUES ("123456789", 1222 , "Math", "Calc 2 Exam 1", "Spring 2016","pdf")')  
connection.commit()

cursor.execute('INSERT INTO Exams VALUES ("000000000", 1120, "English", "Eng 1 Midterms", "Fall 2017","pdf")')
connection.commit()

cursor.execute('INSERT INTO Exams VALUES ("987654321", 2135, "Physics", "Physics 2 Exam 2", "Spring 2018","pdf")')
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