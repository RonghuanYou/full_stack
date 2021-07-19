from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.dojo import Dojo

# display all dojos
@app.route('/dojos')
def index():
    return render_template("/dojos/index.html", all_dojos = Dojo.get_all())

# performing the action of create dojo
@app.route('/dojos/create', methods=['POST'])
def new_dojo():
    Dojo.create(request.form)
    return redirect('/dojos')


# display single dojo
@app.route('/dojo/<int:dojo_id>')
def display_dojo(dojo_id):
    return render_template("dojos/read_one.html", dojo = Dojo.get_one({"id": dojo_id}))


