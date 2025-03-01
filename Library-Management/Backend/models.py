from datetime import datetime
from database import db
class Admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    adminname=db.Column(db.String(50),nullable=False,default='kunal')
    adminemail=db.Column(db.String(50),nullable=False,default='kunalg2022@gmail.com')
    password=db.Column(db.String(50),nullable=False,default='library')
    role=db.Column(db.String(50), nullable=False, default='admin')

class user(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False)
    useremail=db.Column(db.String(50),nullable=False)
    userpassword=db.Column(db.String(50),nullable=False)
    role=db.Column(db.String(50), nullable=False, default='user')

class newuser(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False, unique=True)
    phonenumber=db.Column(db.Integer,nullable=False, unique=True)
    username=db.Column(db.String(50), nullable=False, unique=True)
    password=db.Column(db.String(50),nullable=False)
    confirmpassword=db.Column(db.String(50),nullable=False)
    role=db.Column(db.String(50), nullable=False, default='user')

class ActiveUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)

class GrantRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)

class EBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issued = db.Column(db.Boolean, default=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_of_publish = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(200), nullable=False)
    pdf_filename = db.Column(db.String(200), nullable=False)
    genre= db.Column(db.String(100), nullable=False)
    is_rented = db.Column(db.Boolean, default=False)  

class GrantRequest(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False,default='Pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    grant_date = db.Column(db.DateTime)

    # Relationships
    user = db.relationship('user', backref=db.backref('grant_requests', lazy=True))
    book = db.relationship('Book', backref=db.backref('grant_requests', lazy=True))


