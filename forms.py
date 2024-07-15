from wtforms import SubmitField,BooleanField, StringField, SelectField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Email, NumberRange

class ProductForm(FlaskForm):
    prodName = StringField('Product Name', validators=[DataRequired()])
    prodPrice = IntegerField('Product Price', validators=[DataRequired()])
    prodCurStock = FloatField('Current Stock', validators=[DataRequired()])
    branch = StringField('Branch', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    userName = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = StringField('Contact', validators=[DataRequired()])
    role = IntegerField('Role', validators=[DataRequired()])
    shift = BooleanField('Shift')
    submit = SubmitField('Submit')

class BillForm(FlaskForm):
    tableName = StringField('Table Name', validators=[DataRequired()])
    prodID = IntegerField('Product ID', validators=[DataRequired()])
    totalAmnt = IntegerField('Total Amount', validators=[DataRequired()])
    dateTime = DateTimeField('Date Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    clientID = IntegerField('Client ID', validators=[DataRequired()])
    staffId = IntegerField('Staff ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SaleForm(FlaskForm):
    totalSale = IntegerField('Total Sale', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ClientForm(FlaskForm):
    contact = StringField('Contact', validators=[DataRequired()])
    review = TextAreaField('Review')
    staffId = IntegerField('Staff ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
'''
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=10)])

    email = StringField('Email', validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_field(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=10)])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

    def validate_field(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email  taken')


class Product(FlaskForm):

    prodId = StringField('ProdId', validators=[DataRequired()])
    

'''