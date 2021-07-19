from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.book import Book
from flask_app.models.author import Author


# display all books
@app.route("/books")
def all_books():
    return render_template("books/all_books.html", all_books = Book.get_all())


# performing the action of creating a new book
@app.route("/books/new", methods= ['POST'])
def new_book():
    Book.create(request.form)
    print(request.form)
    # return to book home page
    return redirect("/books")


# read single book
@app.route("/books/<int:book_id>")
def display_book(book_id):
    return render_template(
        "books/read_book.html",
        book = Book.get_one({"id": book_id}),
        all_authors = Author.get_all()
    )

# add author for specific book
@app.route("/books/<int:book_id>/add_author", methods=['POST'])
def add_author(book_id):
    data = {
        "author_id": request.form['author_id'],
        "book_id": book_id
    }
    Book.add_author(data)
    return redirect(f"/books/{book_id}")
