from . import auth
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from .. import db
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('remember', False)

        if remember_me:
            remember_me = True

        user = User.query.filter_by(email=email).first()

        if user is not None and user.verify_password(password):
            login_user(user, remember_me)
            return redirect(url_for('chat.home'))
        flash('邮箱名或密码错误')
        return redirect(url_for('.login'))
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('chat.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form['email'].lower()

        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('该邮箱已经注册，请直接登陆。')
            return redirect(url_for('.login'))

        username = request.form['username']
        password = request.form['password']

        user = User(username=username, email=email)
        user.password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('chat.profile'))

    return render_template('auth/register.html')

