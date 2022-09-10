from app import app, db, Cat
from flask import render_template, request, redirect, url_for, flash, session

@app.route('/cat_add', methods=('GET', 'POST'))
def cat_add():
    if request.method == 'POST':
        name = request.form['name']
        emoji = request.form['emoji']
        color = request.form['color']
        error = None

        if not name:
            error = 'Name is required.'
        elif not emoji:
            error = 'Emoji is required.'
        elif not color:
            error = 'Color is required.'
        
        cat = db.query(Cat).filter_by(name=name, owner_id=session['user_id']).first()
        if cat is not None:
            error = 'You already have a cat with that name.'

        if error is None:
            try:
                cat = Cat(name=name, emoji=emoji, color=color, owner_id=session['user_id'])
                db.add(cat)
                db.commit()
            except:
                error = f"Error occured."
            else:
                flash(f"Successfully added your new cat. You may need to refresh.")
                return redirect(url_for("index"))

        flash(error)

    return render_template('cat_add.html')