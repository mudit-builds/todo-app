from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    done = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()


# Route for the homepage (Add Task)
@app.route("/")
def index():
    return render_template("index.html")


# Route to display all tasks
@app.route("/tasks")
def tasks():
    tasks = Task.query.all()  # Retrieve all tasks from the database
    return render_template("tasks.html", tasks=tasks)


# Route to add a new task
@app.route("/add_task", methods=["POST"])
def add_task():
    title = request.form["title"]
    description = request.form.get("description", "")  # Optional description

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for("tasks"))


# Route to update task status (done/not done)
@app.route("/update_task/<int:task_id>", methods=["POST"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.done = not task.done  # Toggle the done status
        db.session.commit()

    return redirect(url_for("tasks"))  # Redirect back to tasks page


# Route to delete a task
@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for("tasks"))  # Redirect back to the tasks page


if __name__ == "__main__":
    app.run(debug=True)
