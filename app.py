from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'reviews.db')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
CATEGORIES = ['Must Watch', 'Watchable', 'Skip It']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8 MB upload cap

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            summary TEXT NOT NULL,
            details TEXT,
            image TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    conn = get_db()
    reviews = conn.execute('SELECT * FROM reviews ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', reviews=reviews, categories=CATEGORIES)


@app.route('/add', methods=['POST'])
def add_review():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', CATEGORIES[1])
    summary = request.form.get('summary', '').strip()
    details = request.form.get('details', '').strip()
    image_file = request.files.get('image')

    if not title or not summary or category not in CATEGORIES:
        return redirect(url_for('index'))

    filename = None
    if image_file and image_file.filename and allowed_file(image_file.filename):
        ext = image_file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.{ext}")
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = get_db()
    conn.execute(
        'INSERT INTO reviews (title, category, summary, details, image, created_at) '
        'VALUES (?, ?, ?, ?, ?, ?)',
        (title, category, summary, details, filename, datetime.now().strftime('%b %d, %Y'))
    )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/update/<int:review_id>', methods=['POST'])
def update_review(review_id):
    title = request.form.get('title', '').strip()
    category = request.form.get('category', CATEGORIES[1])
    summary = request.form.get('summary', '').strip()
    details = request.form.get('details', '').strip()
    image_file = request.files.get('image')

    if not title or not summary or category not in CATEGORIES:
        return redirect(url_for('index'))

    conn = get_db()

    if image_file and image_file.filename and allowed_file(image_file.filename):
        old_row = conn.execute('SELECT image FROM reviews WHERE id = ?', (review_id,)).fetchone()
        if old_row and old_row['image']:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'], old_row['image'])
            if os.path.exists(old_path):
                os.remove(old_path)
        ext = image_file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.{ext}")
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn.execute(
            'UPDATE reviews SET title=?, category=?, summary=?, details=?, image=? WHERE id=?',
            (title, category, summary, details, filename, review_id)
        )
    else:
        conn.execute(
            'UPDATE reviews SET title=?, category=?, summary=?, details=? WHERE id=?',
            (title, category, summary, details, review_id)
        )

    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    conn = get_db()
    row = conn.execute('SELECT image FROM reviews WHERE id = ?', (review_id,)).fetchone()
    if row and row['image']:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], row['image'])
        if os.path.exists(image_path):
            os.remove(image_path)
    conn.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


init_db()

if __name__ == '__main__':
    app.run(debug=True)
