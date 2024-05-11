from flask import Blueprint, render_template, redirect, url_for, flash, session

from inventory_db import Product
from .forms import LoginForm, RegistrationForm
from .dynamodb_utils import check_credentials, get_user, insert_user

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print("Login page accessed.")  # Debug: initial access
    if form.validate_on_submit():
        print("Form submitted and valid.")  # Debug: form submission validated
        print("Form data:", form.data)  # Debug: print form data
        email = form.email.data.lower().strip()
        password = form.password.data.strip()
        print(f"Attempting to log in with email: {email}, Password: {password}")  # Debug: credentials submitted
        credential_check = check_credentials(email, password)
        print(f"Credentials check returned: {credential_check}")  # Debug: result from check_credentials
        if credential_check:
            print("Credentials verified.")  # Debug: credentials are correct
            session['email'] = email
            flash('Login successful')
            return redirect(url_for('.index'))
        else:
            flash('Invalid email or password', 'error')
            print("Login failed: Invalid email or password.")  # Debug: invalid credentials
    else:
        print("Form not validated.")  # Debug: form validation failed
        print("Errors:", form.errors)  # Debug: print validation errors
    return render_template('login.html', form=form)



@main_bp.route('/index')
def index():
    print("Index page accessed.")  # Debug: index page accessed
    if 'email' in session:
        print(f"Email found in session: {session['email']}")  # Debug: session email present
        user_data = get_user(session['email'])
        products = session.query(Product).all()  # Fetch all products from the database
        print(f"User data retrieved: {user_data}")  # Debug: user data fetched
        return render_template('index.html', user_data=user_data, products=products)
    else:
        print("No email in session, redirecting to login.")  # Debug: session email missing
        return redirect(url_for('.login'))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print("Register page accessed.")  # Debug: register page access
    if form.validate_on_submit():
        print("Registration form submitted.")  # Debug: form submission
        user_data = {
            'email': form.email.data.lower().strip(),
            'address': form.address.data.strip(),
            'name': form.name.data.strip(),
            'password': form.password.data.strip(),  # Consider encrypting this before storage
            'phone': form.phone.data.strip(),
            'postcode': form.postcode.data.strip(),
            'state': form.state.data.strip(),
            'suburb': form.suburb.data.strip()
        }
        print(f"Registration data: {user_data}")  
        if get_user(user_data['email']):
            flash('Email already registered. Please use a different email or login.', 'error')
            print("Email already exists.")  
            return render_template('register.html', form=form)
        
        if insert_user(user_data):
            flash('Registration successful')
            return redirect(url_for('.login'))
        else:
            flash('Failed to register. Please try again.', 'error')
            print("Registration failed.")  
    return render_template('register.html', form=form)

@main_bp.route('/logout')
def logout():
    print("Logging out.")  # Debug: logging out
    session.pop('email', None)
    flash('You have been logged out.')
    return redirect(url_for('.login'))
