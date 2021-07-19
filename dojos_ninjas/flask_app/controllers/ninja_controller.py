from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo


# display form to create ninja
@app.route('/ninjas/new')
def new_ninja():
    return render_template("ninjas/new_ninja.html", all_dojos = Dojo.get_all())


# performing the action of create ninja
@app.route('/ninjas/create', methods=['POST'])
def create_ninja():
    Ninja.create(request.form)
    # get dojo_id, redirect to read one page
    # print(request.form['dojo_id'])
    return redirect('/dojo/'+request.form['dojo_id'])

