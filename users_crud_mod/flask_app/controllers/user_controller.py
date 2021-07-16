from flask import Flask, request, redirect, render_template;
# import my model class, lowercase is file, uppercase is class name Dog
from flask_app import app
from flask_app.models.user import User


@app.route("/")
def index():
    # show usre information we already have, using all_users = User.get_all()
    # get_all() methods in model
    return render_template("read.html", all_users = User.get_all())


@app.route("/new_user_info")
def new_user():
    # display the form to get new user info
    return render_template("create.html")


@app.route("/create", methods=['POST'])
def create_user():
    # on form page, we can submit user info(no duplicate)
    # then we redirect to home page
    # we call classmethod (User.create) here, we store user infor into SQL
    # print(request.form)
    User.create(request.form)
    # TODO: redirect to read one page.
    return redirect('/')


# ---------------
@app.route("/users/<int:user_id>/")
def show(user_id):
    # user is an object
    return render_template("read_one.html", user = User.get_one( {"id": user_id } ))


@app.route("/users/<int:user_id>/edit/")
def display_edit_page(user_id):
    return render_template("edit_user.html", user = User.get_one( {"id": user_id } ))


# performing the action of updating
@app.route("/users/<int:user_id>/update/", methods=['POST'])
def update_user(user_id):
    # updating 
    data_dict = {
        **request.form,
        "id": user_id
    }
    User.update(data_dict)
    # redirect to show page
    return redirect("/users/"+str(user_id))


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    User.delete({"id" : user_id})
    return redirect('/')
