from flask import Blueprint, current_app, render_template, redirect, url_for, flash, session as flask_session
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import scoped_session
from Program.forms import LoginForm, RegistrationForm
from .dynamodb_utils import check_credentials, get_table, get_user, insert_user

DATABASE_URL = "postgresql://postgres:Hoppers3195@assignment3.c54y666q6ct9.ap-southeast-2.rds.amazonaws.com:5432/postgres?sslmode=require"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

main_bp = Blueprint('main', __name__, template_folder='templates')

db_session = scoped_session(Session)

# Define the Product model with QuantityAvailable attribute
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
        table = get_table("Clients")  # Get DynamoDB table object only once
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
        if 'email' in flask_session:
            table = get_table("Clients")
            user_data = get_user(flask_session['email'], table)
            return render_template('index.html', user_data=user_data, products=products)
        else:
            return redirect(url_for('.login'))
    except Exception as e:
        print(f"Error: {e}")
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

@main_bp.route('/logout')
def logout():
    print("Logging out.")  # Debug: logging out
    flask_session.pop('email', None)
    flash('You have been logged out.')
    return redirect(url_for('.login'))
