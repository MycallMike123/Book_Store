from bookstore import app
from flask import render_template, redirect, url_for, flash, request
from bookstore.models import Book, User
from bookstore.forms import RegisterForm, LoginForm, PurchaseBookForm, AddBookForm
from bookstore import db
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')
from flask_login import login_required

@app.route('/bookstore', methods=['GET', 'POST'])
def book_store():
    purchase_form = PurchaseBookForm()

    # Only allow purchase if the user is authenticated
    if request.method == "POST" and current_user.is_authenticated:
        purchased_book = request.form.get('purchased_book')
        p_item_object = Book.query.filter_by(title=purchased_book).first()

        if p_item_object:
            # Check if the user has enough budget to purchase the book
            if current_user.budget >= p_item_object.price:
                p_item_object.owner_id = current_user.id
                current_user.budget -= p_item_object.price
                db.session.commit()
                flash(f"Congratulations! You purchased {p_item_object.title} for {p_item_object.price}", category='success')
            else:
                flash('Insufficient budget to purchase this book.', 'danger')
        else:
            flash('Book not found.', 'warning')
    elif request.method == "POST":
        flash("You need to log in to purchase a book!", category='danger')
        return redirect(url_for('login_page'))

    books = Book.query.all()
    users = User.query.all()
    return render_template('book_store.html', books=books, users=users, purchase_form=purchase_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash('Account created successfully!', category='success')
        return redirect(url_for('book_store'))
    
    if form.errors:
        for err_msgs in form.errors.values():
            for err_msg in err_msgs:
                flash(f'Error occurred while creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('book_store'))
        
        else:
            flash('Username and Password are not a match! please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        # Create a new book instance
        new_book = Book(
            barcode=form.barcode.data,
            title=form.title.data,
            price=form.price.data,
            description=form.description.data,
            owner_id=current_user.id  # Set the owner as the current user
        )
        db.session.add(new_book)
        db.session.commit()
        flash('The book has been added successfully!', 'success')
        return redirect(url_for('book_store'))  # Redirect to bookstore page or another page

    return render_template('add_book.html', form=form)