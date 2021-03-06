"""
    Routes to handel book object in database
    By adding, editing, deleting and displaying 
    individual book in new page from database.
"""
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, current_user
from app import  db
from app.models import *
from app.book.forms import Add_Book, Add_book_to_readinglit
from app.user.forms import LoginForm, RegisterForm
from app.category.forms import Add_Category
from app.publisher.forms import Add_Publisher
from app.author.forms import Add_Author
from app.reading_list.forms import Add_Readinglist

books = Blueprint('books', __name__, url_prefix='/book')

#add book    
@books.route('/book/add', methods=['GET','POST'])
@login_required
def add_book():
    form = Add_Book()
    form_login = LoginForm()
    form_register = RegisterForm()
    form_cat = Add_Category()
    form_publisher = Add_Publisher()
    form_author = Add_Author()
    author = form.author.data
    publisher = form.publisher.data
    category = form.category.data
    if form.validate_on_submit():
        book = Book(title=form.title.data, year=form.year.data, book_cover=form.book_cover.data, description=form.description.data, publisher_id=publisher.PublisherId, category_id=category.CategoryId, author_id=author.AuthorId)
        db.session.add(book)
        db.session.commit()
        flash('New Book has been added!', 'success')
        return redirect(url_for('main.index'))
    return render_template('book/add_book.html', title='New Book', form=form, legend='Add Book', form_login=form_login, form_register=form_register, form_cat=form_cat, form_publisher=form_publisher, form_author=form_author)
    
# individual book page
# add book to reading list
@books.route('/book/<int:book_isbn>', methods=['GET','POST'])
def book(book_isbn):
    form_list = Add_Readinglist()
    form_login = LoginForm()
    form_register=RegisterForm()
    book = Book.query.get_or_404(book_isbn)
    if current_user.is_authenticated:
        form = Add_book_to_readinglit()
        selected_list = form.lists.data
        if request.method == 'POST':
            book.books.append(selected_list)
            db.session.commit()
            flash('New Book has been added to list!', 'success')
            return redirect(url_for('main.index'))
        return render_template('book/book.html', title=book.title, book=book, form=form, form_list=form_list, form_login=form_login, form_register=form_register)
    return render_template('book/book.html', form_list=form_list, title=book.title, book=book, form_login=form_login, form_register=form_register)
    
# edit book information
@books.route('/book/<int:book_isbn>/edit', methods=['GET','POST'])
@login_required
def edit_book(book_isbn):
    book = Book.query.get_or_404(book_isbn)
    form = Add_Book()
    form_login = LoginForm()
    form_register = RegisterForm()
    form_cat = Add_Category()
    form_publisher = Add_Publisher()
    form_author = Add_Author()
    if form.validate_on_submit():
        book.title = form.title.data
        book.year = form.year.data
        book.book_cover = form.book_cover.data
        book.description = form.description.data
        publisher = form.publisher.data
        book.publisher_id = publisher.PublisherId
        category = form.category.data
        book.category_id = category.CategoryId
        author = form.author.data
        book.author_id = author.AuthorId
        db.session.commit()
        flash('The book detailes has been edited!', 'success')
        return redirect(url_for('books.book', book_isbn=book.isbn))
    elif request.method == 'GET':    
        form.title.data = book.title
        form.year.data = book.year
        form.book_cover.data = book.book_cover
        form.description.data = book.description
        form.publisher.data = book.publisher
        form.category.data = book.category
        form.author.data = book.author
    return render_template('book/add_book.html', title='Edit Book', form=form, legend='Edit Book', form_login=form_login, form_register=form_register, form_cat=form_cat, form_publisher=form_publisher, form_author=form_author)
    
# delete book from database
@books.route('/book/<int:book_isbn>/delete', methods=['POST'])
@login_required
def delete_book(book_isbn):
    book = Book.query.get_or_404(book_isbn)
    db.session.delete(book)
    db.session.commit()
    flash('The book has been deleted!', 'success')
    return redirect(url_for('main.index'))