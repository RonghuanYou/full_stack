from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book


class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # MANY-TO-MANY:
        self.books = []
    

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO authors(name)
            VALUES (%(name)s);
        """
        return connectToMySQL("books_schema").query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL("books_schema").query_db(query)

        all_authors = []
        for row in results:
            all_authors.append(cls(row))

        return all_authors


    @classmethod
    def get_one(cls, data):
        # MANY-TO-MANY:
        query = """
            SELECT * FROM authors 
            LEFT JOIN favorites ON authors.id = favorites.author_id
            LEFT JOIN books ON books.id = favorites.book_id
            WHERE authors.id = %(id)s;
        """
        
        results = connectToMySQL("books_schema").query_db(query, data)
        author = cls(results[0])
        print(results)
        if results[0]['books.id'] != None:
            for row in results:
                row_data = {
                    "id": row['books.id'],
                    "title": row['title'],
                    "num_of_pages": row['num_of_pages'],
                    "created_at": row['books.created_at'],
                    "updated_at": row['books.updated_at']
                }
                # author is object, books is list attribute
                author.books.append(book.Book(row_data))
        return author
    
    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        pass

    # MANY-TO-MANY --> ADD BOOK: 
    @classmethod
    def add_book(cls, data):
        query = """
            INSERT INTO favorites (author_id, book_id)
            VALUES (%(author_id)s, %(book_id)s);
        """
        
        return connectToMySQL("books_schema").query_db(query, data)
    