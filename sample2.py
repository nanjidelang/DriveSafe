import sqlite3
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash

DATABASE='/tmp/flaskr.db'
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select Heartrate, SpO2 from entries order by id desc')
    entries = [dict(Heartrate = row[0], SpO2 = row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries = entries)

@app.route('/add', methods = ['POST'])
def add_entry():
    if request.method == 'POST':
        g.db.execute('insert into entries (Heartrate, SpO2) values (?, ?)',[request.form['Heartrate'], request.form['SpO2']])
        g.db.commit()
        return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(debug=True)
