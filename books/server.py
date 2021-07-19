from flask_app import app
from flask_app.controllers import book_controller, author_controller


if __name__ == "__main__":
    app.run(debug=True)
