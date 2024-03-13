from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort

app=Flask(__name__)
app.config['SECRET_KEY'] ='secret'

@app.route('/')

def index():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    return render_template('index.html', events=events)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_event (event_id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?',
                        (event_id,)).fetchone()
    conn.close()
    if event is None:
        abort(404)
    return event

@app.route('/<int:event_id>')

def post(event_id):
    event = get_event(event_id)
    return render_template('post.html', event=event)


@app.route('/create', methods=('GET', 'POST'))

def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO events (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))

def edit(id):
    event = get_event(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE events SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', event= event )

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
        event = get_event(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM events WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('"{}" har tagits bort!'.format(event['title']))
        return redirect(url_for('index'))
