from datetime import datetime
import secrets
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(100),nullable=True)
    username = db.Column(db.String(40), unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    api_token = db.Column(db.String(40))
    
    def __init__(self,username,email,password):
        self.id = str(uuid4())
        self.username = username
        self.email = email.lower()
        self.password = generate_password_hash(password)
        self.api_token = secrets.token_hex(32)
        
                
class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(100),nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow())
    start_date = db.Column(db.DateTime)
    comments = db.Column(db.String(1000))
    labor_hours = db.Column(db.Float(1), default=0)
    emp_id = db.Column(db.Integer)
    status = db.Column(db.String(20),default='New')
    
    
    
    def __init__(self,d):
        for k,v in d.items():
            getattr(self,k)
            setattr(self,k,v)
        
    def to_dict(self):
        return {k:v for k,v in vars(self).items() if k != '_sa_instance_state'}

    def update(self,d):
        for k,v in d.items():
            getattr(self,k)
            setattr(self,k,v)
        
    