#Greg fixed this new App when he travelled, I had fixed my own earlier & think I can work with mine
#worst I delete my application.py and rename this one application.py 
#and delete my database.py and his databaseGregNew.py to database.py
from bottle import route, post, run, template, redirect, request

import databaseGregNew

@route("/")
def get_index():
    redirect("/list")

@route("/list")
def get_list():
    items = databaseGregNew.get_items()
    return template("list.tpl", shopping_list=items)

@route("/add")
def get_add():
    return template("add_item.tpl")

@post("/add")
def post_add():
    description = request.forms.get("description")
    databaseGregNew.add_item(description)
    redirect("/list")

@route("/delete/<id>")
def get_delete(id):
    databaseGregNew.delete_item(id)
    redirect("/list")

@route("/update/<id>")
def get_update(id):
    items = databaseGregNew.get_items(id)
    if len(items) != 1:
        redirect("/list")
    description = items[0]['description']
    return template("update_item.tpl", id=id, description=description)

@post("/update")
def post_update():
    description = request.forms.get("description")
    id = request.forms.get("id")
    databaseGregNew.update_item(id, description)
    redirect("/list")

run(host='localhost', port=8080)