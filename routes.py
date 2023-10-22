from app import app

from flask import render_template, redirect, request, url_for, session, flash

from jinja2 import Template

import helpers, timefunctions

import subforums, discussions, messages, users, comments

current_template = []

@app.route("/")
def index():
    sub_type = subforums.ITEM_TYPE
    disc_type = discussions.ITEM_TYPE

    session['url'] = url_for("index")
    sub_list = subforums.get_list()
    disc_list = discussions.get_list()

    return render_template("index.html", featuring=helpers.sort_by_date_newest(sub_list+disc_list), sub_type=sub_type, disc_type=disc_type)


@app.route("/sub/<int:id>")
def sub(id):
    session['url'] = url_for("sub", id=id)
    print("WENT TO SUB", id)
    list = discussions.get_list_by_sub_id(id)
    sub = subforums.get_sub(id)
    return render_template("subforum.html", sub=sub, sub_admin=users.get_username(sub.user_id), discussions=list)


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
    print("SUB ID:", subforum_id)
    discussions.create_new_discussion(title, content, subforum_id, user_id)
    return redirect("/sub/"+subforum_id)


@app.route("/sub/<int:sub_id>/discussion/<int:disc_id>")
def discussion(sub_id, disc_id):
    session['url'] = url_for("discussion", sub_id=sub_id, disc_id=disc_id)
    list = comments.get_list_by_id(disc_id)
    disc = discussions.get_discussion(disc_id)
    print(disc_id)
    return render_template("discussion.html", discussion=disc, comments=list, user_id=disc.user_id, sub_id=sub_id)



@app.route("/sub/<int:sub_id>/discussion/<int:disc_id>/new_comment")
def new_comment(sub_id, disc_id):
    session['url'] = url_for("new_comment", sub_id=sub_id, disc_id=disc_id)
    return render_template("new_comment.html", sub_id=sub_id, disc_id=disc_id)


@app.route("/create_comment", methods=["POST"])
def create_comment():
    content = request.form["content"]
    sub_id = request.form["sub_id"]
    disc_id = request.form["disc_id"]
    if content:
        print(content)
        print(sub_id)
        print(disc_id)
        user_id = users.session_user_id()
        comments.create_new_comment(content, disc_id, user_id)
        return redirect("/sub/"+sub_id+"/discussion/"+disc_id)
    else:
        return redirect(session["url"])


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
    sub_type = subforums.ITEM_TYPE
    disc_type = discussions.ITEM_TYPE
    comt_type = comments.ITEM_TYPE

    session['url'] = url_for("profile", id=id)
    user = users.get_user_by_id(id)
    activity = helpers.sort_by_date_newest(users.get_user_activity(id))

    return render_template("profile_overview.html", user=user, activity=activity, sub_type=sub_type, disc_type=disc_type, comt_type=comt_type)


@app.route("/profile/<int:id>/about")
def profile_about(id):
    session['url'] = url_for("profile_about", id=id)
    user = users.get_user_by_id(id)

    return render_template("profile_about.html", user=user)


@app.route("/profile/<int:id>/subforums")
def profile_subforums(id):
    session['url'] = url_for("profile_subforums", id=id)
    user = users.get_user_by_id(id)
    subs = subforums.get_list_by_user_id(id)

    return render_template("profile_subforums.html", user=user, subforums=subs)


@app.route("/profile/<int:id>/discussions")
def profile_discussions(id):
    session['url'] = url_for("profile_discussions", id=id)
    user = users.get_user_by_id(id)
    discs = discussions.get_list_by_user_id(id)

    return render_template("profile_discussions.html", user=user, discussions=discs)


@app.route("/profile/<int:id>/comments")
def profile_comments(id):
    session['url'] = url_for("profile_comments", id=id)
    user = users.get_user_by_id(id)
    comnts = comments.get_list_by_user_id(id)

    return render_template("profile_comments.html", user=user, comments=comnts)


@app.route("/users")
def explore_users():
    session['url'] = url_for("explore_users")
    list = users.get_list()
    return render_template("users.html", users=list)


@app.route("/subforums")
def explore_subforums():
    session['url'] = url_for("explore_subforums")
    list = subforums.get_list()
    return render_template("subforums.html", subforums=list)


@app.route("/discussions")
def explore_discussions():
    session['url'] = url_for("explore_subforums")
    list = discussions.get_list()
    return render_template("discussions.html", discussions=list)

@app.route("/result")
def result():
    query = request.args["query"]
    option = request.args["sort_by"]
    print(query, option)
    sort_option = ""

    if option == "newest":
        sort_option = "created_at DESC"

    elif option == "oldest":
        sort_option = "created_at ASC"

    elif option == "most_followed":
        #########################
        sort_option = "followers"

    #sql = f"SELECT id, content FROM messages WHERE content LIKE :query ORDER BY {sort_option}"
    #result = db.session.execute(sql, {"query":"%"+query+"%"})
    #messages = result.fetchall()
    print("SORT OPTION:", sort_option)
    return render_template("index.html")


@app.route("/logout")
def logout():
    users.logout()
    return redirect(session["url"])


@app.context_processor
def unil_processor():
    def get_time_ago(time):
        return timefunctions.convert_time(time)
    
    def get_user_by_id(id):
        return users.get_user_by_id(id)
    
    def get_sub_by_id(id):
        return subforums.get_sub(id)
    
    def get_discussion_by_id(id):
        return discussions.get_discussion(id)
    
    return dict(get_time_ago=get_time_ago, get_user_by_id=get_user_by_id, get_sub_by_id=get_sub_by_id, get_discussion_by_id=get_discussion_by_id)