from app import app

from flask import render_template, redirect, request, url_for, session, flash

import subforums, discussions, messages, users, comments


@app.route("/")
def index():
    session['url'] = url_for("index")
    list = subforums.get_list()
    user_id = users.session_user_id()
    print("USER ID", user_id)
    return render_template("index.html", subforums=list)


@app.route("/sub/<int:id>")
def sub(id):
    session['url'] = url_for("sub", id=id)
    print("WENT TO SUB", id)
    list = discussions.get_list_by_sub_id(id)
    sub = subforums.get_sub(id)
    return render_template("subforum.html", title=sub.title, content=sub.content, sub_username=users.get_username(sub.user_id), discussions=list, id=id)


@app.route("/new_sub")
def new_sub():
    session['url'] = url_for("new_sub")
    return render_template("new_sub.html")


@app.route("/create_sub", methods=["POST"])
def create_sub():
    title = request.form["title"]
    content = request.form["content"]
    user_id = users.session_user_id()
    subforums.create_new_sub(title, content, user_id)
    return redirect("/")


@app.route("/sub/<int:id>/new_discussion")
def new_discussion(id):
    session['url'] = url_for("new_discussion", id=id)
    return render_template("new_discussion.html", id=id)


@app.route("/create_discussion", methods=["POST"])
def create_discussion():
    title = request.form["title"]
    content = request.form["content"]
    user_id = users.session_user_id()
    subforum_id = request.form["sub_id"]
    discussions.create_new_discussion(title, content, subforum_id, user_id)
    return redirect("/sub/"+subforum_id)


@app.route("/sub/<int:sub_id>/discussion/<int:disc_id>")
def discussion(sub_id, disc_id):
    session['url'] = url_for("discussion", sub_id=sub_id, disc_id=disc_id)
    list = comments.get_list_by_id(disc_id)
    disc = discussions.get_discussion(disc_id)
    return render_template("discussion.html", title=disc.title, content=disc.content, comments=list, sub_id=sub_id, id=disc_id)


@app.route("/sub/<int:sub_id>/discussion/<int:disc_id>/new_comment")
def new_comment(sub_id, disc_id):
    session['url'] = url_for("new_comment", sub_id=sub_id, disc_id=disc_id)
    return render_template("new_comment.html", sub_id=sub_id, disc_id=disc_id)


@app.route("/create_comment", methods=["POST"])
def create_comment():
    content = request.form["content"]
    sub_id = request.form["sub_id"]
    disc_id = request.form["disc_id"]
    user_id = users.session_user_id()
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
            return redirect(session["url"])
        else:
            if users.does_username_exist(username):
                error = "Wrong password!"
            else:
                error = "Username does not exist!"
            return render_template("login.html", name_value=username, pass_value=password, error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    template_name = "register.html"
    username = None
    password1 = None
    password2 = None
    error = None
    name_min = users.USERNAME_MIN
    name_max = users.USERNAME_MAX
    pass_min = users.PASSWORD_MIN
    pass_max = users.PASSWORD_MAX

    if request.method == "GET":
        return render_template(template_name, name_min=name_min, name_max=name_max, pass_min=pass_min, pass_max=pass_max)
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        name_ok = users.is_username_ok(username)
        pass_ok = users.is_password_ok(password1)

        if name_ok and pass_ok:
            if password1 == password2:
                if users.register(username, password1):
                    return redirect(session["url"])
                else:
                    error = "Username is taken! Try another username."
            else:
                error = "Make sure the passwords match!"
        else:
            if name_ok:
                error = f"Make sure your password is in correct form!"
            elif pass_ok:
                error = f"Make sure your username is in correct form!"
            else:
                error = f"Make sure your username and password are in correct forms!"
    if error:
        return render_template(template_name, name_min=name_min, name_max=name_max, pass_min=pass_min, pass_max=pass_max, name_value=username, pass_value1=password1, pass_value2=password2, error=error)


@app.route("/profile/<int:id>", methods=["GET", "POST"])
def profile(id):
    session['url'] = url_for("profile", id=id)
    user = users.get_user_by_id(id)
    return render_template("profile.html", user=user)


@app.route("/logout")
def logout():
    users.logout()
    return redirect(session["url"])