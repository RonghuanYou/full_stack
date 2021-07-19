from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book

# display all authors 
@app.route("/authors")
def all_authors():
    return render_template("authors/all_authors.html", all_authors = Author.get_all())

# performing the action of creating a new author
@app.route("/authors/new", methods=['POST'])
def new_author():
    Author.create(request.form)
    return redirect("/authors")

# read single author 
# pass all_books info, not for specific author's favorite book

@app.route("/author/<int:author_id>")
def display_author(author_id):
    return render_template(
        "authors/read_author.html",
        author = Author.get_one({"id": author_id}),
        all_books = Book.get_all()
    )

# add book as author's favorates
# MANY-TO-MANY
@app.route("/authors/<int:author_id>/add_book", methods=['POST'])
def add_book(author_id):
    data = {
        "book_id": request.form['book_id'],
        "author_id": author_id
    }
    Author.add_book(data)
    return redirect(f"/author/{author_id}")
