from app import app
from flask import render_template, redirect, request
import subforums, discussions, messages, users, comments

@app.route("/")
def index():
    list = subforums.get_list()
    user_id = users.session_user_id()
    print("USER ID", user_id)
    return render_template("index.html", subforums=list)

#Siirrytään subiin
@app.route("/sub/<int:id>")
def sub(id):
    print("WENT TO SUB", id)
    list = discussions.get_list_by_sub_id(id)
    sub = subforums.get_sub(id)
    return render_template("subforum.html", title=sub.title, content=sub.content, sub_username=users.get_username(sub.user_id), discussions=list, id=id)

#Siirrytään uuden subin luontiin
@app.route("/new_sub")
def new_sub():
    return render_template("new_sub.html")

#Luodaan subi
@app.route("/create_sub", methods=["POST"])
def create_sub():
    title = request.form["title"]
    content = request.form["content"]
    user_id = users.session_user_id()
    subforums.create_new_sub(title, content, user_id)
    return redirect("/")

#Siirrytään keskustelun luontiin
@app.route("/new_discussion/<int:id>")
def new_discussion(id):
    return render_template("new_discussion.html", id=id)

#Luodaan keskustelu
@app.route("/create_discussion", methods=["POST"])
def create_discussion():
    title = request.form["title"]
    content = request.form["content"]
    user_id = users.session_user_id()
    subforum_id = request.form["sub_id"]
    discussions.create_new_discussion(title, content, subforum_id, user_id)
    return redirect("/")

@app.route("/sub/<int:sub_id>/discussion/<int:disc_id>")
def discussion(sub_id, disc_id):
    list = comments.get_list_by_id(disc_id)
    disc = discussions.get_discussion(disc_id)
    return render_template("discussion.html", title=disc.title, content=disc.content)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            print("LOGIN OK")
            return redirect("/")
        else:
            print("LOGIN NOT OK")
            return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("register.html")
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/profile/<int:id>", methods=["GET", "POST"])
def profile(id):
    
    return render_template("profile.html")