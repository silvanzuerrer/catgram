from app import app, db, Cat, CatWeight
from flask import render_template, request, redirect, url_for, flash, session
from datetime import date

@app.route('/cat_weight_add', methods=('GET', 'POST'))
def cat_weight_add():
    if request.method == 'POST':
        name = request.form['name']
        weight = request.form['weight']
        error = None

        if not name:
            error = 'Name is required.'
        elif not weight:
            error = 'Weight is required.'
        
        cat = db.query(Cat).filter_by(name=name, owner_id=session['user_id']).first()
        if cat is None:
            error = 'You do not have a cat with that name.'

        if error is None:
            try:
                cat_weight = CatWeight(cat_id=cat.id, weight_grams=weight, date=date.today())
                db.add(cat_weight)
                db.commit()
            except:
                error = f"Error occured."
            else:
                flash(f"Successfully added your new cat's weight. You may need to refresh.")
                return redirect(url_for("index"))

        flash(error)

    return render_template('cat_weight_add.html')