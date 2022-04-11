from requests import delete
from sqlalchemy import ForeignKey
from app import db, login
from flask_login import UserMixin
from datetime import datetime
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from werkzeug.security import generate_password_hash, check_password_hash

cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
)

@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column (db.String(50), unique= True, nullable=False)
    email= db.Column (db.String(50), unique= True, nullable=False)
    password= db.Column (db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    phones = db.relationship('Phone', backref='user', lazy='dynamic')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User|{self.username}>"

    def __str__(self):
        return self.username
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(20), unique= True, nullable=False)
    body= db.Column(db.String(255))
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post|{self.title}>"

class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(100), nullable=False)
    last_name=db.Column(db.String(100), nullable=False)
    phone_number=db.Column(db.String(100), nullable=False)
    city=db.Column(db.String(15), nullable=False)
    date_created= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    image_url = db.Column(db.String(100), default ='https://via.placeholder.com/500')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs.get('image'):
            self.upload_to_cloudinary(kwargs['image'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Phone {self.id}|{self.first_name}>"

    def __str__(self):
        return f"""
        FirstName:{self.first_name}
        LastName:{self.last_name}
        Phone:{self.phone_number}
        City:{self.city}
        """
    
    def upload_to_cloudinary(self,file_to_upload):
        image_info= cloudinary.uploader.upload(file_to_upload)
        self.image_url=image_info.get('url')

    # def update(self, **kwargs):
    #     for key, value in kwargs.items():
    #         if key in {'title', 'body'}:
    #             setattr(self, key, value)
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()