"""
    Routes to handel publishre object in database
    By adding, editing, deleting and displaying 
    list of all publishers from database.
"""
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required
from app import  db
from app.models import Publisher, Book
from app.publisher.forms import Add_Publisher

publishers = Blueprint('publishers', __name__, url_prefix='/publisher')

# display list of publishers
@publishers.route('/publisher')
@login_required
def all_publishers():
    publishers = Publisher.query.all()
    return render_template('publisher/publishers.html', publishers=publishers, title='Publishers')
    
# individual publisher route
@publishers.route('/publisher/<int:publisher_id>')
@login_required
def publisher(publisher_id):
    publisher = Publisher.query.get_or_404(publisher_id)
    return render_template('publisher/publisher.html', title=publisher.Name, publisher=publisher)
    
#add publisher    
@publishers.route('/publisher/add', methods=['GET','POST'])
@login_required
def add_publisher():
    form = Add_Publisher()
    if form.validate_on_submit():
        publisher = Publisher(Name=form.Name.data)
        db.session.add(publisher)
        db.session.commit()
        flash('New Publisher has been added!', 'success')
        return redirect(url_for('publishers.all_publishers'))
    return render_template('publisher/add_publisher.html', title='New Publisher', form=form, legend='Add Publisher Name')
    
# edit publishers name
@publishers.route('/publisher/<int:publisher_id>/edit', methods=['GET','POST'])
@login_required
def edit_publisher(publisher_id):
    publisher = Publisher.query.get_or_404(publisher_id)
    form = Add_Publisher()
    if form.validate_on_submit():
        publisher.Name = form.Name.data
        db.session.commit()
        flash('The publisher name has been updated!', 'success')
        return redirect(url_for('publishers.all_publishers', publisher_id=publisher.PublisherId))
    elif request.method == 'GET': 
        form.Name.data = publisher.Name
    return render_template('publisher/add_publisher.html', title='Edit Publisher ', form=form, legend='Edit Publisher Name')
    
# delete publishers from database
@publishers.route('/publisher/<int:publisher_id>/delete',  methods=['GET','POST'])
@login_required
def delete_publisher(publisher_id):
    publisher = Publisher.query.get_or_404(publisher_id)
    db.session.delete(publisher)
    db.session.commit()
    flash('The publisher has been deleted!', 'success')
    return redirect(url_for('publishers.all_publishers'))
    
# display all books from the publisher    
@publishers.route('/publisher/<string:Name>')
def publisher_books(Name):
    page = request.args.get('page', 1, type=int)
    publisher_query = Publisher.query.filter_by(Name=Name).first_or_404()
    books = Book.query.filter_by(publisher=publisher_query).order_by(Book.isbn.desc()).paginate(page=page, per_page=6)
    return render_template('publisher/publisher_books.html',books=books, publisher=publisher_query)
