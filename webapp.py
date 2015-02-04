from flask import Flask, render_template, request, url_for
import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    hackbright.connect_to_db()
    student_github = request.args.get("github")
    fname, lname, gname = hackbright.get_student_by_github(student_github)
    grades = hackbright.show_all_grades(fname, lname)
    html = render_template("student_info.html", first_name=fname,
                                                last_name=lname,
                                                github=gname, 
                                                grades=grades)

    return html


@app.route("/project")
def show_project():
    hackbright.connect_to_db()
    title = request.args.get("title")
    headers, students = hackbright.get_grades_by_project(title)
    # percentage = (students[2]/headers[1])

    html = render_template("show_project.html", title=title,
                                                description=headers[0],
                                                max_grade=headers[1],
                                                students=students,)

    return html


@app.route("/")
def get_github():
    return render_template("get_github.html")


if __name__ == "__main__":
    app.run(debug=True)