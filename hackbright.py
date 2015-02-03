import sqlite3

DB = None
CONN = None


def make_new_student(first_name, last_name, github):
    query = """INSERT into Students (first_name, last_name, github) values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Succesfully added student: %s %s"%(first_name, last_name)


def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])


def make_new_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Succesfully added project: %s"%(title)


def get_project_by_title(title):
    query = """SELECT title, description FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Title: %s
Description: %s"""%(row[0], row[1])


def add_new_grade(first_name, last_name, project, points):
    print first_name, last_name, project, points

    query1 = """ SELECT id FROM Students WHERE first_name = ? AND last_name = ?"""
    DB.execute(query1, (first_name, last_name))
    stu_id = DB.fetchone()[0]

    print "stu_id = ", stu_id

    query2 = """ SELECT id FROM Projects WHERE title = ?"""
    DB.execute(query2, (project,))
    pro_id = DB.fetchone()[0]

    print "pro_id = ", pro_id


    query3 = """INSERT into Grades (stu_id, pro_id, points) values (?, ?, ?)"""
    DB.execute(query3, (stu_id, pro_id, points))
    CONN.commit()

    print "Succesfully added grade: %s for project: %s"%(points, project)



def get_grade_by_student(first_name, last_name, project):
    query1 = """ SELECT id FROM Students WHERE first_name = ? AND last_name = ?"""
    DB.execute(query1, (first_name, last_name))
    stu_id = DB.fetchone()[0]

    query = """SELECT points, max_grade FROM Grades JOIN Projects ON pro_id=Projects.id 
    WHERE stu_id = ? AND title = ?"""  
    
    DB.execute(query, (stu_id, project))
    row = DB.fetchone()
    
    print """\
%s %s's grade for %s is %d"""%(first_name, last_name, project, row[0])


def show_all_grades(first_name, last_name):
    query1 = """ SELECT id FROM Students WHERE first_name = ? AND last_name = ?"""
    DB.execute(query1, (first_name, last_name))
    stu_id = DB.fetchone()[0]  

    query = """SELECT title, points, max_grade 
    FROM Projects JOIN Grades on pro_id=Projects.id 
    WHERE stu_id = ? """
    DB.execute(query, (stu_id,))
    row = DB.fetchall()

    for project in row:
        print """\
Title: %s
Points: %d 
Max Grade: %d """%(project[0], project[1], project[2])


def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()


def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(', ')
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "get_grade":
            get_grade_by_student(*args)
        elif command == "add_grade":
            add_new_grade(*args)
        elif command == "show_grades":
            show_all_grades(*args)

    CONN.close()

if __name__ == "__main__":
    main()
