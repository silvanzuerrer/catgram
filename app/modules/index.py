from app import app, db, Cat, CatWeight
from flask import render_template

@app.route('/')
def index():
    cats = db.query(Cat)
    cat_weights = db.query(CatWeight)
    return render_template('index.html', cats=cats, cat_weights=cat_weights)