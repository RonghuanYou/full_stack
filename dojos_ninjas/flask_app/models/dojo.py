from flask.globals import request
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja

class Dojo:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # contains ninja objects
        self.ninjas = []
    
    
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO dojos (name)
            VALUES (%(name)s);
        """
        return connectToMySQL("dojos_schema").query_db(query, data)        


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL("dojos_schema").query_db(query)        

        all_dojos = []
        for row in results:
            all_dojos.append(cls(row))
        return all_dojos


    @classmethod
    def get_one(cls, data):
        # # ONE TO MANY: merge dojos table and ninjas table
        query = """
            SELECT * FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojo_id
            WHERE dojos.id = %(id)s;
        """
        results = connectToMySQL("dojos_schema").query_db(query, data)
        # return cls(results[0])

        # ONE TO MANY: add ninja data into ninja object
        # results[0] is dict with info of two tables
        dojo = cls(results[0])

        for row in results:
            # row_data: get ninjas row data and push them to ninja.Ninja list
            row_data = {
                "id": row['ninjas.id'],
                # it doesn't need dojo id because we already have dojo(put it in ninja file)
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "age": row['age'],
                "created_at": row['ninjas.created_at'],
                "updated_at": row['ninjas.created_at']
            }
            # dojo.ninjas -> object.ninja (lst)
            dojo.ninjas.append(ninja.Ninja(row_data))
        return dojo

    @classmethod
    def update(cls, data):
        pass


    @classmethod
    def delete(cls, data):
        pass

