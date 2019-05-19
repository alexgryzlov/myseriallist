from flask import render_template, url_for, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required

from myseriallist import app, db
from myseriallist.forms import RegistrationForm, LoginForm, SerialForm, AddSerialForm
from myseriallist.models import User, Serial, Connection


@app.route("/")
@app.route("/home/")
def home():
    page = request.args.get('page', default=1, type=int)
    serials = Serial.query.paginate(page=page, per_page=5)
    return render_template('home.html', serials=serials)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('home')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(username=form.email.data).first()
        if user:
            pass
        elif email:
            pass
        else:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('home')
    form = LoginForm()
    if form.validate_on_submit():
        valid_user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if valid_user:
            login_user(valid_user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title="about")


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile/<string:username>", methods=["GET", "POST"])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('profile.html', title='Profile', user=user)
    else:
        abort(404)


@app.route("/serial/<int:serial_id>", methods=["GET", "POST"])
def serial(serial_id):
    added = Connection.query.filter_by(user_id=current_user.get_id(), serial_id=serial_id).first()
    serial = Serial.query.get_or_404(serial_id)
    form = SerialForm()
    if form.add_to_list.data:
        connection = Connection(user_id=current_user.user_id, serial_id=serial_id)
        db.session.add(connection)
        db.session.commit()
        return redirect(request.url)
    if form.update.data:
        added.watch_status = form.watch_status.data
        added.series_watched = form.series_watched.data
        db.session.commit()
        return redirect(request.url)

    if added:
        form.watch_status.data = added.watch_status
        form.series_watched.data = added.series_watched

    return render_template('serial.html', title=serial.title, serial=serial, form=form, added=added)


@app.route("/add_serial", methods=["GET", "POST"])
@login_required
def add_serial():
    form = AddSerialForm()
    if form.validate_on_submit():
        serial = Serial(title=form.title.data, series_number=form.series_number.data, description=form.description.data)
        if not Serial.query.filter_by(title=serial.title).first():
            db.session.add(serial)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add_serial.html', title='Add Serial', form=form)


@app.route("/profile/<string:username>/list", methods=["GET", "POST"])
def serial_list(username):
    user = User.query.filter_by(username=username).first()
    serials = Connection.query.filter_by(user_id=user.user_id).all()
    serial_data = {}
    for serial in serials:
        serial_data[serial.serial_id] = Serial.query.filter_by(serial_id=serial.serial_id).first()
    return render_template('serial_list.html', title=username + '\'s Serial List', serials=serials,
                           serial_data=serial_data)
