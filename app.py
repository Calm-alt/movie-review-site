from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
CATEGORIES = ["Must Watch", "Watchable", "Skip It"]

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

# ============================
# DATABASE
# ============================

database_url = os.environ.get("DATABASE_URL")

if not database_url:
    database_url = "sqlite:///reviews.db"

# Render compatibility
if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ============================
# DATABASE MODEL
# ============================

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    summary = db.Column(
        db.Text,
        nullable=False
    )

    details = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.String(50),
        nullable=False
    )


with app.app_context():
    db.create_all()


# ============================
# HELPERS
# ============================

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ============================
# HOME PAGE
# ============================

@app.route("/")
def index():

    reviews = (
        Review.query
        .order_by(Review.id.desc())
        .all()
    )

    return render_template(
        "index.html",
        reviews=reviews,
        categories=CATEGORIES
    )
    
# ============================
# ADD REVIEW
# ============================

@app.route("/add", methods=["POST"])
def add_review():

    title = request.form.get("title", "").strip()
    category = request.form.get("category", CATEGORIES[1])
    summary = request.form.get("summary", "").strip()
    details = request.form.get("details", "").strip()

    image_file = request.files.get("image")

    if not title or not summary or category not in CATEGORIES:
        return redirect(url_for("index"))

    filename = None

    if (
        image_file
        and image_file.filename
        and allowed_file(image_file.filename)
    ):
        ext = image_file.filename.rsplit(".", 1)[1].lower()

        filename = secure_filename(
            f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.{ext}"
        )

        image_file.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

    review = Review(
        title=title,
        category=category,
        summary=summary,
        details=details,
        image=filename,
        created_at=datetime.now().strftime("%b %d, %Y")
    )

    db.session.add(review)
    db.session.commit()

    return redirect(url_for("index"))


# ============================
# UPDATE REVIEW
# ============================

@app.route("/update/<int:review_id>", methods=["POST"])
def update_review(review_id):

    review = Review.query.get_or_404(review_id)

    title = request.form.get("title", "").strip()
    category = request.form.get("category", CATEGORIES[1])
    summary = request.form.get("summary", "").strip()
    details = request.form.get("details", "").strip()

    image_file = request.files.get("image")

    if not title or not summary or category not in CATEGORIES:
        return redirect(url_for("index"))

    review.title = title
    review.category = category
    review.summary = summary
    review.details = details

    if (
        image_file
        and image_file.filename
        and allowed_file(image_file.filename)
    ):

        if review.image:

            old_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                review.image
            )

            if os.path.exists(old_path):
                os.remove(old_path)

        ext = image_file.filename.rsplit(".", 1)[1].lower()

        filename = secure_filename(
            f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.{ext}"
        )

        image_file.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

        review.image = filename

    db.session.commit()

    return redirect(url_for("index"))

# ============================
# DELETE REVIEW
# ============================

@app.route("/delete/<int:review_id>", methods=["POST"])
def delete_review(review_id):

    review = Review.query.get_or_404(review_id)

    if review.image:

        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            review.image
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(review)
    db.session.commit()

    return redirect(url_for("index"))


# ============================
# RUN
# ============================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )