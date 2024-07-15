from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy import select




# Example function to handle creating a new order (bill)
def create_order(prodID, totalAmnt):
    try:
        # Begin transaction
        with db.session.begin():
            # Load the product with a lock for update
            product = Product.query.options(joinedload(Product.prodCurStock)).filter(Product.prodID == prodID).with_for_update().first()
            
            # Update stock
            if product:
                product.prodCurStock -= totalAmnt
                db.session.add(Bill(prodID=prodID, totalAmnt=totalAmnt))  # Assuming Bill model is defined
                db.session.commit()
                return True, "Order created successfully"
            else:
                return False, "Product not found"
    except Exception as e:
        db.session.rollback()
        return False, str(e)


class Product(db.Model):
    prodID = db.Column(db.Integer, primary_key=True)
    prodName = db.Column(db.String(50), unique=True, nullable=False)
    prodPrice = db.Column(db.Integer, nullable=False)
    prodCurStock = db.Column(db.Float, nullable=False)
    branch = db.Column(db.String(50), nullable=False)  # Added branch field

    def __init__(self, prodName, prodPrice, prodCurStock, branch):
        self.prodName = prodName
        self.prodPrice = prodPrice
        self.prodCurStock = prodCurStock
        self.branch = branch


class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.Integer, nullable=False)  # Assuming role is an integer
    shift = db.Column(db.Boolean, default=False, nullable=False)
    invites = db.relationship('Client', backref='staff', lazy=True)
    bills = db.relationship('Bill', backref='staff', lazy=True)


from sqlalchemy import event

class Bill(db.Model):
    billID = db.Column(db.Integer, primary_key=True)
    tableName = db.Column(db.String(50), nullable=False)
    prodID = db.Column(db.Integer, db.ForeignKey('product.prodID'), nullable=False)
    totalAmnt = db.Column(db.Integer, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    clientID = db.Column(db.Integer, db.ForeignKey('client.clientID'), nullable=False)
    staffId = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)

    # Function to handle reducing product stock when a bill is created
    def reduce_product_stock(self):
        product = Product.query.get(self.prodID)
        if product:
            product.prodCurStock -= self.totalAmnt
            db.session.commit()

# SQLAlchemy event listener to automatically reduce stock when a bill is created
@event.listens_for(Bill, 'after_insert')
def update_product_stock_on_bill_insert(mapper, connection, bill):
    bill.reduce_product_stock()
from sqlalchemy.orm import joinedload

# Example: Eager loading relationships
bills = Bill.query.options(joinedload(Bill.product)).all()





class Sale(db.Model):
    saleID = db.Column(db.Integer, primary_key=True)
    totalSale = db.Column(db.Integer, nullable=False)
    bills = db.relationship('Bill', backref='sale', lazy=True)

class Client(db.Model):
    clientID = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(20), unique=True, nullable=False)
    review = db.Column(db.String(100))  # Assuming review is a text field
    staffId = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)


from datetime import datetime, timedelta
from sqlalchemy import func

one_week_ago = datetime.utcnow() - timedelta(weeks=1)

weekly_sales = db.session.query(
    User.userName,
    func.sum(Product.prodPrice * Bill.totalAmnt).label('total_sales')
).join(Bill, User.userID == Bill.staffId).join(Product, Bill.prodID == Product.prodID)\
.filter(Bill.dateTime >= one_week_ago)\
.group_by(User.userName)\
.order_by(func.sum(Product.prodPrice * Bill.totalAmnt).desc())\
.all()

top_seller = db.session.query(
    User.userName,
    func.sum(Product.prodPrice * Bill.totalAmnt).label('total_sales')
).join(Bill, User.userID == Bill.staffId).join(Product, Bill.prodID == Product.prodID)\
.group_by(User.userName)\
.order_by(func.sum(Product.prodPrice * Bill.totalAmnt).desc())\
.first()



'''
class Bill(db.Model):
    billID = db.Column(db.Integer, primary_key=True)
    tableName = db.Column(db.String(50), nullable=False)
    prodID = db.Column(db.Integer, db.ForeignKey('product.prodID'), nullable=False)
    totalAmnt = db.Column(db.Integer, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    clientID = db.Column(db.Integer, db.ForeignKey('client.clientID'), nullable=False)
    staffId = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    saleID = db.Column(db.Integer, db.ForeignKey('sale.saleID'), nullable=False)



class Product(db.Model):
    prodID = db.Column(db.Integer, primary_key=True)
    prodName = db.Column(db.String(50), unique=True, nullable=False)
    prodPrice = db.Column(db.Integer, nullable=False)
    prodCurStock = db.Column(db.Float, nullable=False)
class Bill(db.Model):
    billID = db.Column(db.Integer, primary_key=True)
    tableName = db.Column(db.String(50), nullable=False)
    prodID = db.Column(db.Integer, db.ForeignKey('product.prodID'), nullable=False)
    totalAmnt = db.Column(db.Integer, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    clientID = db.Column(db.Integer, db.ForeignKey('client.clientID'), nullable=False)
    staffId = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
class Sale(db.Model):
    saleID = db.Column(db.Integer, primary_key=True)
    totalSale = db.Column(db.Integer, nullable=False)
    bills = db.relationship('Bill', backref='sale', lazy=True)
'''
