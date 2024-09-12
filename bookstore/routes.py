from bookstore import app
from flask import render_template
from bookstore.models import Book, User

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/bookstore')
def book_store():
    books = Book.query.all()
    users = User.query.all()
    return render_template('book_store.html', books=books, users=users)