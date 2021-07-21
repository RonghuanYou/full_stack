from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


# display form to create recipe
@app.route("/recipes/new")
def new_recipe():
    return render_template("recipes/new_recipe.html")


# performing the action of creating recipe
@app.route("/recipes/create", methods=['POST'])
def create_recipe():
    if not Recipe.recipe_validate(request.form):
        return redirect("/recipes/new")

    userID = int(request.form['user_id'])
    data = {
        **request.form,
        'user_id': userID
    }
    Recipe.create(data)
    return redirect("/dashboard")


# display all recipe instructions 
@app.route("/recipes/<int:recipe_id>")
def display_instruction(recipe_id):
    return render_template(
        "recipes/instruction.html", 
        user=User.get_one({"id": session['uuid']}),
        recipe = Recipe.get_one({"id": recipe_id})    
    )

# display form to edit recipe
@app.route("/recipes/edit/<int:recipe_id>")
def edit_recipe(recipe_id):
    return render_template("recipes/edit_recipe.html", recipe=Recipe.get_one({"id": recipe_id}))


# performing the action of updating new info to specific recipe
@app.route("/recipes/update/<int:recipe_id>", methods=['POST'])
def update_recipe(recipe_id):
    if not Recipe.recipe_validate(request.form):
        return redirect(f"/recipes/edit/{recipe_id}")

    data = {
        **request.form, 
        "id": recipe_id, 
    }
    Recipe.update(data)
    return redirect("/dashboard")


# delete recipe
@app.route("/recipes/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    Recipe.delete({"id": recipe_id})
    return redirect("/dashboard")
