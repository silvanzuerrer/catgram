import functools
from app import app, db, User
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                user = User(username=username, password=generate_password_hash(password))
                db.add(user)
                db.commit()
            except exc.IntegrityError:
                error = f"User {username} is already registered."
            else:
                flash(f"Successfully registered, please login. You may need to refresh.")
                return redirect(url_for("login"))

        flash(error)

    return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.query(User).filter_by(username=username).first()

        if user is None:
           error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
           error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            session['user_username'] = user.username
            flash(f"Successfully logged in. You may need to refresh.")
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
