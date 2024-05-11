from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email'), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    submit = SubmitField('Login')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            print("Form validation failed:", self.errors)
        else:
            print("Form validated successfully")
        return rv

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email'), Length(min=6, max=40)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=255)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    phone = StringField('Phone', validators=[DataRequired(), Regexp(r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    postcode = StringField('Postcode', validators=[DataRequired(), Regexp(r'^\d{4,5}$', message="Invalid postcode")])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=40)])
    suburb = StringField('Suburb', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Register')


