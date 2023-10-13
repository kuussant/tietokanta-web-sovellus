from app import app
from flask import render_template, redirect, request, url_for, session
import subforums, discussions, messages, users, comments

@app.route("/")
def index():
    session['url'] = url_for("index")
    list = subforums.get_list()
    user_id = users.session_user_id()
    print("USER ID", user_id)
    return render_template("index.html", subforums=list)

#Siirrytään subiin
@app.route("/sub/<int:id>")
def sub(id):
    session['url'] = url_for("sub", id=id)
    print("WENT TO SUB", id)
    list = discussions.get_list_by_sub_id(id)
    sub = subforums.get_sub(id)
    return render_template("subforum.html", title=sub.title, content=sub.content, sub_username=users.get_username(sub.user_id), discussions=list, id=id)

#Siirrytään uuden subin luontiin
@app.route("/new_sub")
def new_sub():
    session['url'] = url_for("new_sub")
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
@app.route("/sub/<int:id>/new_discussion")
def new_discussion(id):
    session['url'] = url_for("new_discussion", id=id)
    return render_template("new_discussion.html", id=id)

#Luodaan keskustelu
@app.route("/create_discussion", methods=["POST"])
def create_discussion():
    title = request.form["title"]
    content = request.form["content"]
    user_id = users.session_user_id()
    subforum_id = request.form["sub_id"]
    discussions.create_new_discussion(title, content, subforum_id, user_id)
    return redirect("/sub/"+subforum_id)

#Keskustelu
@app.route("/sub/<int:sub_id>/discussion/<int:disc_id>")
def discussion(sub_id, disc_id):
    session['url'] = url_for("discussion", sub_id=sub_id, disc_id=disc_id)
    print(f"================== SUB_ID = {sub_id} DISC_ID = {disc_id} USER_ID = {users.session_user_id()} ===================")
    list = comments.get_list_by_id(disc_id)
    disc = discussions.get_discussion(disc_id)
    return render_template("discussion.html", title=disc.title, content=disc.content, comments=list, sub_id=sub_id, id=disc_id)

@app.route("/sub/<int:sub_id>/discussion/<int:disc_id>/new_comment")
def new_comment(sub_id, disc_id):
    session['url'] = url_for("new_comment", sub_id=sub_id, disc_id=disc_id)
    print(f"==================== ADDING COMMENT SUB_ID = {sub_id} DISC_ID = {disc_id} ======================")
    return render_template("new_comment.html", sub_id=sub_id, disc_id=disc_id)

@app.route("/create_comment", methods=["POST"])
def create_comment():
    content = request.form["content"]
    sub_id = request.form["sub_id"]
    disc_id = request.form["disc_id"]
    user_id = users.session_user_id()
    print(f"================== WROTE COMMENT SUB_ID = {sub_id} DISC_ID = {disc_id} USER_ID = {user_id} ===================")
    comments.create_new_comment(content, disc_id, user_id)
    return redirect("/sub/"+sub_id+"/discussion/"+disc_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            print("LOGIN OK")
            return redirect(session["url"])
        else:
            print("LOGIN NOT OK")
            return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if len(username) > 3 and password > 5:
            if users.register(username, password):
                return redirect(session["url"])
            else:
                error = "Username is taken"
                return render_template("register.html")

            
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect(session["url"])

@app.route("/profile/<int:id>", methods=["GET", "POST"])
def profile(id):
    session['url'] = url_for("profile", id=id)
    return render_template("profile.html")