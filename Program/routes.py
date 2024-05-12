from urllib.parse import urlencode, parse_qs, unquote
from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request, jsonify, session as flask_session
import json
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
import urllib3
from Program.forms import LoginForm, RegistrationForm
from .dynamodb_utils import check_credentials, get_table, get_user, insert_user

DATABASE_URL = "postgresql://postgres:Hoppers3195@assignment3.c54y666q6ct9.ap-southeast-2.rds.amazonaws.com:5432/postgres?sslmode=require"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

main_bp = Blueprint('main', __name__, template_folder='templates')

db_session = scoped_session(Session)

class Product(Base):
    __tablename__ = 'products'
    ProductID = Column(Integer, primary_key=True)
    ProductName = Column(String(100), nullable=False)
    Description = Column(String(250))
    Price = Column(Float)
    Category = Column(String(50))
    ImageURL = Column(String(200))

class Inventory(Base):
    __tablename__ = 'inventory'
    InventoryID = Column(Integer, primary_key=True)
    ProductID = Column(Integer, ForeignKey('products.ProductID'), nullable=False)
    QuantityAvailable = Column(Integer)
    SupplierID = Column(Integer)
    WarehouseLocation = Column(String(100))

@main_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        password = form.password.data.strip()
        table = get_table("Clients")
        credential_check = check_credentials(email, password, table)
        if credential_check:
            flask_session['email'] = email
            flash('Login successful')
            return redirect(url_for('.index'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@main_bp.route('/index')
def index():
    try:
        products = db_session.query(Product, Inventory.QuantityAvailable).join(Inventory, Product.ProductID == Inventory.ProductID).all()
        user_details = None
        if 'email' in flask_session:
            table = get_table("Clients")
            user_data = get_user(flask_session['email'], table)
            if user_data:
                user_details = {
                    'name': user_data.get('name', 'User'),
                    'address': user_data.get('address', ''),
                    'suburb': user_data.get('suburb', ''),
                    'state': user_data.get('state', ''),
                    'postcode': user_data.get('postcode', ''),
                    'phone': user_data.get('phone', '')
                }
                return render_template('index.html', user_details=user_details, products=products)
        flash('Please log in to view this page', 'error')
        return redirect(url_for('.login'))
    except Exception as e:
        current_app.logger.error(f"Error in index: {e}")
        return render_template('error.html', error=str(e))
    finally:
        db_session.remove()

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_data = {
            'email': form.email.data.lower().strip(),
            'address': form.address.data.strip(),
            'name': form.name.data.strip(),
            'password': form.password.data.strip(),
            'phone': form.phone.data.strip(),
            'postcode': form.postcode.data.strip(),
            'state': form.state.data.strip(),
            'suburb': form.suburb.data.strip()
        }
        table = get_table("Clients")
        if get_user(user_data['email'], table):
            flash('Email already registered. Please use a different email or login.', 'error')
            return render_template('register.html', form=form)

        if insert_user(user_data, table):
            flash('Registration successful')
            return redirect(url_for('.login'))
        else:
            flash('Failed to register. Please try again.', 'error')
    return render_template('register.html', form=form)

from flask import session

def calculate_total_price(cart_items):
    total_price = 0
    for item in cart_items:
        product = db_session.query(Product).filter_by(ProductID=item['productId']).first()
        if product:
            total_price += product.Price * item['quantity']
    return total_price

@main_bp.route('/place-order', methods=['POST'])
def place_order():
    try:
        cart_items = json.loads(request.form.get('cartItems'))
        user_details = json.loads(request.form.get('userDetails'))
        
        current_app.logger.debug(f"Received cart items: {cart_items}")
        current_app.logger.debug(f"Received user details: {user_details}")

        if not cart_items or not user_details:
            flash('Missing cart items or user details.', 'error')
            return redirect(url_for('.index'))

        session['cart_items'] = json.dumps(cart_items)  
        session['user_details'] = json.dumps(user_details)  
        total_price = calculate_total_price(cart_items)
        session['total_price'] = total_price

        return redirect(url_for('.order_confirmation'))
    except Exception as e:
        current_app.logger.error(f"Error processing your order: {str(e)}")
        flash('Error processing your order: {}'.format(str(e)), 'error')
        return redirect(url_for('.index'))



@main_bp.route('/order-confirmation')
def order_confirmation():
    try:
        if 'cart_items' not in session or 'user_details' not in session:
            flash('Order data missing.', 'error')
            return redirect(url_for('.index'))

        cart_items = json.loads(session.get('cart_items', '[]'))
        user_details = json.loads(session.get('user_details', '{}'))
        total_price = session.get('total_price', 0)

        return render_template('order_confirmation.html', cart_items=cart_items, user_details=user_details, total_price=total_price)
    except Exception as e:
        current_app.logger.error(f"Error displaying order confirmation: {str(e)}")
        flash('Error displaying order confirmation: {}'.format(str(e)), 'error')
        return redirect(url_for('.index'))


@main_bp.route('/logout')
def logout():
    flask_session.pop('email', None)
    flash('You have been logged out.')
    return redirect(url_for('main.login'))
