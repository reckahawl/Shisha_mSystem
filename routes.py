from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import RegistrationForm, ProductForm
from app.models import User, Product

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/weekly_sales')
def weekly_sales():
    one_week_ago = datetime.utcnow() - timedelta(weeks=1)

    # Query to calculate total sales for each staff member in the last week
    sales_data = db.session.query(
        User.userName,
        db.func.sum(Product.prodPrice * Bill.totalAmnt).label('total_sales')
    ).join(Bill, User.userID == Bill.staffId).join(Product, Bill.prodID == Product.prodID)\
    .filter(Bill.dateTime >= one_week_ago)\
    .group_by(User.userName).all()

    return render_template('weekly_sales.html', sales_data=sales_data)

@app.route('/product', methods=['GET', 'POST'])
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            prodName=form.prodName.data,
            prodPrice=form.prodPrice.data,
            prodCurStock=form.prodCurStock.data,
            branch=form.branch.data
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('form.html', form=form)

@app.route('/user', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(
            userName=form.userName.data,
            email=form.email.data,
            contact=form.contact.data,
            role=form.role.data,
            shift=form.shift.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('form.html', form=form)

@app.route('/bill', methods=['GET', 'POST'])
def create_bill():
    form = BillForm()
    if form.validate_on_submit():
        new_bill = Bill(
            tableName=form.tableName.data,
            prodID=form.prodID.data,
            totalAmnt=form.totalAmnt.data,
            dateTime=form.dateTime.data,
            clientID=form.clientID.data,
            staffId=form.staffId.data
        )
        db.session.add(new_bill)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('form.html', form=form)

@app.route('/sale', methods=['GET', 'POST'])
def create_sale():
    form = SaleForm()
    if form.validate_on_submit():
        new_sale = Sale(
            totalSale=form.totalSale.data
        )
        db.session.add(new_sale)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('form.html', form=form)

@app.route('/client', methods=['GET', 'POST'])
def create_client():
    form = ClientForm()
    if form.validate_on_submit():
        new_client = Client(
            contact=form.contact.data,
            review=form.review.data,
            staffId=form.staffId.data
        )
        db.session.add(new_client)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('form.html', form=form)

@app.route('/success')
def success():
    return "Form submitted successfully!"



@app.route('/create_bill', methods=['GET', 'POST'])
def create_bill():
    bill_form = BillForm()
    if bill_form.validate_on_submit():
        # Store the bill form data in session
        session['bill_data'] = {
            'staffName': bill_form.staffName.data,
            'clientName': bill_form.clientName.data,
            'tableName': bill_form.tableName.data
        }
        return redirect(url_for('add_product'))
    return render_template('create_bill.html', form=bill_form)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    product_form = ProductForm()
    if product_form.validate_on_submit():
        # Retrieve bill form data from session
        bill_data = session.get('bill_data')
        if not bill_data:
            flash('Bill information is missing. Please start over.')
            return redirect(url_for('create_bill'))

        # Find the staff and client
        staff = User.query.filter_by(userName=bill_data['staffName']).first()
        client = Client.query.filter_by(contact=bill_data['clientName']).first()

        # Find the product
        product = Product.query.filter_by(prodName=product_form.prodName.data).first()

        if not (staff and client and product):
            flash('Invalid staff, client, or product information. Please check your inputs.')
            return redirect(url_for('create_bill'))

        # Create a new bill
        new_bill = Bill(
            tableName=bill_data['tableName'],
            prodID=product.prodID,
            totalAmnt=product_form.amountConsumed.data,
            clientID=client.clientID,
            staffId=staff.userID
        )

        # Update product stock
        product.prodCurStock -= product_form.amountConsumed.data

        # Save to database
        db.session.add(new_bill)
        db.session.commit()

        flash('Bill created successfully!')
        return redirect(url_for('create_bill'))

    return render_template('add_product.html', form=product_form)


from flask import Flask, request, jsonify, render_template
from flask_classful import FlaskView, route

app = Flask(__name__)

class BillView(FlaskView):
    route_base = '/bill'  # Base URL for this view

    @route('/create', methods=['GET', 'POST'])
    def create(self):
        if request.method == 'POST':
            staff_name = request.form['staff_name']
            client_name = request.form['client_name']
            table_name = request.form['table_name']
            # Handle form submission, save to database, etc.
            return jsonify({'status': 'Bill created successfully'})
        return render_template('create_bill.html')

    @route('/add_product', methods=['POST'])
    def add_product(self):
        product_data = request.get_json()
        # Handle product data submission, save to database, etc.
        return jsonify({'status': 'Product added successfully'})

BillView.register(app)

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Bill(Resource):
    def post(self):
        staff_name = request.form['staff_name']
        client_name = request.form['client_name']
        table_name = request.form['table_name']
        # Handle form submission, save to database, etc.
        return {'status': 'Bill created successfully'}

class Product(Resource):
    def post(self):
        product_data = request.get_json()
        # Handle product data submission, save to database, etc.
        return {'status': 'Product added successfully'}

api.add_resource(Bill, '/bill/create')
api.add_resource(Product, '/bill/add_product')

from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/cached_bills')
@cache.cached(timeout=60)
def cached_bills():
    bills = Bill.query.all()
    return render_template('bills.html', bills=bills)

@dbg.route('/')
def home():
    return render_template('home.html')



@dbg.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)



@dbg.route('/admin')
@login_required



@dbg.route('/user')



@dbg.route('/update_stock')



@dbg.route('/update_bill')



@dbg.route('/create_bill')
def bill():
    form
    return('/bill')

@dbg.route('/create_sale')
def sale():
    form 
    return('/sale')
