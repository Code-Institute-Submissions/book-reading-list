"""
    Create database tables by using the SQLAlchamy syntax. 
    This helps to map the tables and columns to classes and objects respectively. The types of the column can be passed as an argument.
"""
from datetime import datetime
from app import db

# many-to-many relationships 
author_book = db.Table('author_book', 
            db.Column('AuthorId', db.Integer, db.ForeignKey('author.AuthorId')),
            db.Column('isbn', db.Integer, db.ForeignKey('book.isbn'))
)

book_reading = db.Table('book_reading',
            db.Column('isbn', db.Integer, db.ForeignKey('book.isbn'), primary_key=True),
            db.Column('ListId', db.Integer, db.ForeignKey('readingList.ListId'), primary_key=True)
)

# Author Class/Model
class Author(db.Model):
    AuthorId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100), nullable=False)
    LastName = db.Column(db.String(100), nullable=False)
    
    def __init__(self, FirstName, LastName):
        self.FirstName = FirstName
        self.LastName = LastName
        
# Publisger Class/Model
class Publisher(db.Model):
    PublisherId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    book = db.relationship('Book', backref='publisher', lazy=True)
    
    def __init__(self, Name):
        self.Name = Name
        
# Category Class/Model
class Category(db.Model):
    CategoryId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    book = db.relationship('Book', backref='category', lazy=True)
    
    def __init__(self, Name):
        self.Name = Name
        
# Book Class/Model
class Book(db.Model):
    isbn = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.DateTime, nullable=False, default=datetime.year)
    book_cover = db.Column(db.String(255), nullable=False)
    publisher_id= db.Column(db.Integer, db.ForeignKey('publisher.PublisherId'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.CategoryId'), nullable=False)
    authors = db.relationship('Author', secondary=author_book, backref=db.backref('writer', lazy='dynamic'))
    readers = db.relationship('ReadingList', secondary=book_reading, backref=db.backref('reader', lazy='dynamic'))
    
    def __init__(self, Title, year, book_cover):
        self.Title = Title
        self.year = year
        self.book_cover = book_cover
    
# User Class/Model
class User(db.Model):
    UserId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(255),nullable=False)
    userName = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reading_list = db.relationship('ReadingList', backref='user', lazy=True)
    
    def __init__(self, FirstName,userName,password):
        self.FirstName = FirstName    
        self.userName = userName
        self.password = password
        
    def __repr__(self):
        return '<User %r>' % self.userName
        

#Rading List Class/Model
class ReadingList(db.Model):
    ListId = db.Column(db.Integer, primary_key=True)
    ListName = db.Column(db.String(255), nullable=False)
    UserId = db.Column(db.Integer, db.ForeignKey('user.UserId'))
    
    def __init__(self, ListName):
        self.ListName = ListName
    