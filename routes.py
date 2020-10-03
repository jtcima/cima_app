from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from app import app, login, db
from models import User, Contacts
from form import RegistrationForm, LoginForm, ContactForm
from werkzeug.urls import url_parse
from cimabot import cimabot
from sqlalchemy.exc import IntegrityError
import time

#user loader
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm(meta={'csrf': True})
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('log_in'))
        login_user(user, remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['Get', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm(meta={'csrf':True})
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now registered! Please log in')
            return redirect(url_for('log_in'))
        except IntegrityError:
            flash('Hmmm...username already exists, please try another username.')
    return render_template('register.html', title='Register', form=form)

@login.unauthorized_handler
def unauthorized():
    print('Sorry you must log in to have chat.')
    return redirect(url_for('log_in'))

@app.route('/logout')
@app.route('/home/contacts/after/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

@app.route("/", methods=["GET"])
def index():
    
    return render_template('index.html')

@app.route("/home", methods=["GET"])
@login_required
def home():
    return render_template('home.html')

@app.route("/home/get", methods=["GET", "POST"])
def get_bot_response():        
    userText = request.args.get('msg')
    return str(cimabot.get_response(userText))
    #if request.args:
        #userText = request.args.get('msg')
        #return chatbot.respond(userText)
    #else:
        #return chatbot.respond('')
    
@app.route("/home/contacts", methods=["GET","POST"])
@app.route("/home/contacts/", methods=["GET","POST"])
@login_required
def add_contacts():
    form=ContactForm(meta={'csrf': True})
    if form.validate_on_submit():
        contact = Contacts(name=form.name.data, email=form.email.data,
                            phone_no=form.phone.data, enquires = form.enquires.data)
        db.session.add(contact)
        db.session.commit()   
        flash('Thank you for your enquiry! we will be in touch with you:)') 
        return redirect(url_for('after_contacts'))
    return render_template('contacts.html', form=form)

@app.route("/home/contacts/after", methods=["GET"])
@app.route("/home/contacts/after/", methods=["GET"])
@login_required
def after_contacts():
    return render_template('after_contacts.html')