from datetime import timedelta
from urllib.parse import urlparse, urljoin
from flask import current_app as app, render_template, flash, redirect, url_for, abort, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_login_example import db, login_manager, photos
from flask_login_example.models import User, Profile
from flask_login_example.forms import LoginForm, ProfileForm, SignupForm


@app.route('/', methods=['GET'])
def index():
    """ Returns the home page."""
    return render_template('index.html')


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'


@login_manager.user_loader
def load_user(user_id):
    """ Takes a user ID and returns a user object or None if the user does not exist"""
    if user_id is not None:
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
        return user
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm(request.form)
    if signup_form.validate_on_submit():
        user = User(first_name=signup_form.first_name.data,
                    last_name=signup_form.last_name.data,
                    email=signup_form.email.data)
        user.set_password(signup_form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(f"Hello, {user.first_name} {user.last_name}. You are signed up.")
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {signup_form.email.data}. ', 'error')
            return redirect(url_for('signup'))
        return redirect(url_for('index'))
    return render_template('signup.html', title='Sign Up', form=signup_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=login_form.email.data)).scalar_one_or_none()
        login_user(user, remember=login_form.remember.data, duration=timedelta(minutes=1))
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('index'))
    return render_template('login.html', title='Login', form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Find the profile of the logged in user if it exists
    profile = db.session.execute(db.select(Profile).filter_by(user_id=current_user.id)).scalar_one_or_none()
    photo_fn = ''
    if profile:
        # Create a form and populate with the current profile and if there is one, the name of the photo
        form = ProfileForm(obj=profile)
        if profile.photo:
            photo_fn = profile.photo
    else:
        form = ProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        filename = None
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                filename = photos.save(request.files['photo'])
        p = Profile(username=form.username.data, photo=filename, bio=form.bio.data,
                    user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('display_profiles', username=p.username))
    return render_template('profile.html', form=form, photo_filename=photo_fn)


@app.route('/display_profiles', methods=['POST', 'GET'], defaults={'username': None})
@app.route('/display_profiles/<username>/', methods=['POST', 'GET'])
@login_required
def display_profiles(username):
    results = None
    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for("index"))
            results = Profile.query.filter(Profile.username.contains(term)).all()
    else:
        results = Profile.query.filter_by(username=username).all()
    if not results:
        flash("Username not found.")
        return redirect(url_for("index"))
    filenames = []
    for result in results:
        if result.photo:
            filename = result.photo
            filenames.append(filename)
    return render_template('display_profile.html', profiles=zip(results, filenames))
