from app import app

from flask import render_template, redirect, request, url_for, session, flash

from jinja2 import Template

import helpers, timefunctions

import subforums, discussions, messages, users, comments

current_template = []

sub_type = subforums.ITEM_TYPE
disc_type = discussions.ITEM_TYPE
comt_type = comments.ITEM_TYPE
user_type = users.ITEM_TYPE

@app.route("/")
def index():
    sub_type = subforums.ITEM_TYPE
    disc_type = discussions.ITEM_TYPE

    session['url'] = url_for("index")
    url_before()
    sub_list = subforums.get_list()
    disc_list = discussions.get_list()

    return render_template("index.html", featuring=helpers.sort_by_date_newest(sub_list+disc_list), sub_type=sub_type, disc_type=disc_type)


########################## SUBFORUMS #######################################


@app.route("/sub/<int:id>")
def sub(id):
    session['url'] = url_for("sub", id=id)
    print("WENT TO SUB", id)
    list = discussions.get_list_by_sub_id(id)
    sub = subforums.get_sub(id)
    followers = subforums.get_followers(id)
    print(len(followers))
    return render_template("subforum_overview.html", sub=sub, followers=len(followers), sub_admin=users.get_username(sub.user_id), discussions=list)


@app.route("/sub/<int:id>/manage")
def sub_manage(id):
    session['url'] = url_for("sub_manage", id=id)
    sub = subforums.get_sub(id)
    
    return render_template("subforum_manage.html", sub=sub)


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


@app.route("/update/sub/<int:id>", methods=["POST"])
def update_sub(id):
    title = request.form["title"]
    content = request.form["content"]

    print("YEET")
    subforums.update_contents(id, title, content)

    return redirect(session["url"])


@app.route("/follow/sub/<int:id>")
def sub_follow(id):
    subforums.follow(id, users.session_user_id())
    return redirect(session['url'])


@app.route("/unfollow/sub/<int:id>")
def sub_unfollow(id):
    subforums.unfollow(id, users.session_user_id())
    return redirect(session['url'])


@app.route("/delete/sub/<int:id>")
def sub_delete(id):
    return render_template("confirm.html", item=subforums.get_sub(id), sub_type=sub_type, disc_type=disc_type, comt_type=comt_type)


########################## DISCUSSIONS #######################################


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
    url_before()
    session['url'] = url_for("discussion", sub_id=sub_id, disc_id=disc_id)
    list = comments.get_list_by_id(disc_id)
    disc = discussions.get_discussion(disc_id)
    print(disc_id)
    return render_template("discussion.html", discussion=disc, comments=list, user_id=disc.user_id, sub_id=sub_id)


@app.route("/sub/<int:sub_id>/discussion/<int:disc_id>/new_comment")
def new_comment(sub_id, disc_id):
    url_before()
    session['url'] = url_for("new_comment", sub_id=sub_id, disc_id=disc_id)
    return render_template("new_comment.html", sub_id=sub_id, disc_id=disc_id)


@app.route("/delete/discussion/<int:id>")
def discussion_delete(id):
    print("DISCUSSING", discussions.get_discussion(id).item_type)

    return render_template("confirm.html", item=discussions.get_discussion(id), sub_type=sub_type, disc_type=disc_type, comt_type=comt_type)


########################## COMMENTS #######################################


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


@app.route("/delete/comment/<int:id>")
def comment_delete(id):
    return render_template("confirm.html", item=comments.get_comment(id), sub_type=sub_type, disc_type=disc_type, comt_type=comt_type)


########################## USERS #######################################

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

    url_before()
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


@app.route("/profile/<int:id>/following")
def profile_following(id):
    session['url'] = url_for("profile_following", id=id)
    user = users.get_user_by_id(id)
    list = subforums.get_user_followed_subs(id)

    return render_template("profile_following.html", user=user, subforums=list)


@app.route("/delete/profile/<int:id>")
def profile_delete(id):
    item = users.get_user_by_id(id)
    return render_template("confirm.html", item=item)


########################## EXPLORE #######################################


@app.route("/subforums")
def explore_subforums():
    session['url'] = url_for("explore_subforums")
    url_before()
    list = subforums.get_list()
    return render_template("subforums.html", subforums=list)


@app.route("/discussions")
def explore_discussions():
    session['url'] = url_for("explore_discussions")
    url_before()
    list = discussions.get_list()
    return render_template("discussions.html", discussions=list)


@app.route("/users")
def explore_users():
    session['url'] = url_for("explore_users")
    url_before()
    list = users.get_list()
    return render_template("users.html", users=list)


@app.route("/result")
def result():
    query = request.args["query"]
    option = request.args["sort_by"]
    type = request.args["item_type"]

    print(type)
    if type == sub_type:
        list = subforums.search_by(query, option)
        return render_template("subforums.html", subforums=list)
    
    if type == disc_type:
        list = discussions.search_by(query, option)
        return render_template("discussions.html", discussions=list)

    if type == user_type:
        option2 = request.args["order_by"]
        list = users.search_by(query, option, option2)
        return render_template("users.html", users=list)

    return render_template("index.html")


@app.route("/logout")
def logout():
    users.logout()
    return redirect(session["url"])


@app.route("/confirm_delete", methods=["POST"])
def confirm_delete():
    item_id = request.form["item_id"]
    item_type = request.form["item_type"]

    session_user_id = users.session_user_id()

    print(item_id, item_type)

    if item_type == sub_type:
        subforums.delete(item_id, session_user_id)

    elif item_type == disc_type:
        discussions.delete(item_id, session_user_id)

    elif item_type == comt_type:
        comments.delete(item_id, session_user_id)
    
    elif item_type == users.ITEM_TYPE:
        pass
    
    return redirect(session["url_before"])


def url_before():
    session['url_before'] = session['url']
    print("URL_BEFORE", session['url_before'])


@app.context_processor
def unil_processor():

    def list_len(list):
        return len(list)
    
    def get_time_ago(time):
        return timefunctions.convert_time(time)
    
    def get_user_by_id(id):
        return users.get_user_by_id(id)
    
    def get_session_user_id():
        return users.session_user_id()
    
    def get_session_username():
        return users.session_username()
    
    def get_is_admin(id):
        return users.is_admin(id)
    
    def get_sub_by_id(id):
        return subforums.get_sub(id)
    
    def get_discussion_by_id(id):
        return discussions.get_discussion(id)
    
    def does_user_follow_sub(sub_id, user_id, visible_false):
        return subforums.does_user_follow_sub(sub_id, user_id, visible_false)
    
    return dict(list_len=list_len, get_time_ago=get_time_ago, get_user_by_id=get_user_by_id, get_session_user_id=get_session_user_id, get_session_username=get_session_username, get_is_admin=get_is_admin, get_sub_by_id=get_sub_by_id, get_discussion_by_id=get_discussion_by_id, does_user_follow_sub=does_user_follow_sub)