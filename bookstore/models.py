from bookstore import db

# Define the User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Relationship to Book model
    books = db.relationship('Book', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

# Define the Book model
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Foreign key to the User table
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"