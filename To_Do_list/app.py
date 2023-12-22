from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'db.sqlite'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_text = request.form['task_text']
    db = get_db()
    db.execute('INSERT INTO tasks (task_text, completed) VALUES (?, ?)', (task_text, 0))
    db.commit()
    return redirect(url_for('index'))

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    db = get_db()
    db.execute('UPDATE tasks SET completed = ? WHERE id = ?', (1, task_id))
    db.commit()
    return redirect(url_for('index'))

def create_tasks_table():
    connection = sqlite3.connect(app.config['DATABASE'])
    cursor = connection.cursor()

    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_text TEXT NOT NULL,
            completed BOOLEAN NOT NULL
        )
    '''

    cursor.execute(create_table_sql)
    connection.commit()
    connection.close()

# Call the function to create the table when the script is run
create_tasks_table()

# ... (rest of your Flask code)

if __name__ == '__main__':
    app.run(debug=True)