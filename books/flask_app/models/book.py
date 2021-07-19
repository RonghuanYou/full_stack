from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # MANY-TO-MANY
        self.authors = []
    
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO books(title, num_of_pages)
            VALUES (%(title)s, %(num_of_pages)s);
        """
        return connectToMySQL("books_schema").query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL("books_schema").query_db(query)

        all_books = []
        for row in results:
            all_books.append(cls(row))
        return all_books


    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM books WHERE id = %(id)s;"
    #     results = connectToMySQL("books_schema").query_db(query, data)
    #     # convert the first dict to object
    #     # return cls(results[0])
    #     # MANY-TO-MANY: ADD BOOK INFO IN AUTHOR OBJECT
    #     return cls(results[0])

    @classmethod
    def get_one(cls, data):
        # MANY-TO-MANY:
        query = """
            SELECT * FROM books 
            LEFT JOIN favorites ON books.id = favorites.book_id
            LEFT JOIN authors ON authors.id = favorites.author_id
            WHERE books.id = %(id)s;
        """
        results = connectToMySQL("books_schema").query_db(query, data)
        print(results[0])

        book = cls(results[0])
        if results[0]['authors.id'] != None:
            for row in results:
                row_data = {
                    "id": row['authors.id'],
                    "name": row['name'],
                    "created_at": row['authors.created_at'],
                    "updated_at": row['authors.updated_at']
                }
                # book is object, authors is list attribute
                book.authors.append(author.Author(row_data))
        return book


    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        pass

    # for controller passing data
    @classmethod
    def add_author(cls, data):
        query = """
            INSERT INTO favorites (author_id, book_id)
            VALUES (%(author_id)s, %(book_id)s);
        """
        return connectToMySQL("books_schema").query_db(query, data)

