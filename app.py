from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
def count_characters(text):
    return len(text)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title'].strip()
        desc = request.form['desc'].strip()
        if count_characters(title) < 4:
            flash("Title must contain 4-5 characters.", "error")
            return redirect("/")
        if count_characters(desc) < 10:
            flash("Description must contain 10-15 characters.", "error")
            return redirect("/")
        if not title or not desc:
            err_msg = "Please fill all the fields"
            return render_template('index.html', err_msg=err_msg)
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodos = Todo.query.all()

    return render_template('index.html', allTodos=allTodos)

@app.route("/show")
def products():
    allTodos = Todo.query.all()
    print(allTodos)
    return render_template("show.html", allTodos=allTodos)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        query_words = query.split()
        results = Todo.query.filter(
            Todo.title.ilike(f"%{query}%") | 
            Todo.desc.ilike(f"%{query}%")
        ).all()

        if len(query_words) >= 2:
            middle_words = ' '.join(query_words[len(query_words) // 2 - 1 : len(query_words) // 2 + 1])
            additional_results = Todo.query.filter(
                Todo.desc.ilike(f"%{middle_words}%")
            ).all()
            results = list({todo.sno: todo for todo in results + additional_results}.values())

        # Recommendations based on the first 3 characters
        recommendations = Todo.query.filter(
            Todo.title.ilike(f"{query[:3]}%") | 
            Todo.desc.ilike(f"{query[:3]}%")
        ).all()
    else:
        results = Todo.query.all()
        recommendations = []

    return render_template(
        'index.html',
        allTodos=results,
        recommendations=recommendations,
        search_query=query,
    )

if __name__ == "__main__":
    app.run(debug=True, port=4000)
