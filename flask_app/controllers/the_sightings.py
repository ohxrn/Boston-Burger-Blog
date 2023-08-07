from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

@app.route("/make_sighting", methods=['post'])
def collect():
    if not Sighting.validate_sighting(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/make_sightings')
    # else no errors:
    sight_data={**request.form,
            'user_id':session['user_id']}
    Sighting.save_recipe(sight_data)
    
    return redirect("/go_to_read")

@app.route("/make_sightings")
def collection():
    return render_template("sightings.html")

@app.route("/delete/<int:id>")
def delete(id):
    data5={'id':id}
    Sighting.delete(data5)
    return redirect("/go_to_read")

@app.route("/edit/<int:id>")
def edit(id):
    data_id={'id':id}
    edit=Sighting.get_one(data_id)
    print("THIS IS EDIT------------------------------------------>",edit)

    information= Sighting.get_both()
    return render_template("edit_page.html",edit=edit, information=information)

@app.route("/edit_sighting/<int:id>", methods=['post'] )
def edit_return(id):
    data_return={
        **request.form,
        'id':id }
    Sighting.edit(data_return)
    return redirect("/go_to_main")


@app.route("/go_to_main")
def edit_calculate():
    
    information= Sighting.get_both()
    return render_template("success.html",edit=edit, information=information)

@app.route("/the_page")
def relink():
    return render_template("success.html")




@app.route("/go_to_read")
def display_page():
   information= Sighting.get_both()
   
   return render_template("success.html", information=information)

@app.route("/single_sighting/<int:id>")
def recipe(id):
  
    data5={
        'id':id
    }
    wild=Sighting.get_one(data5)
    return render_template("single_sighting.html", wild=wild)



