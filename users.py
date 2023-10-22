import db, helpers

from flask import session

from werkzeug.security import check_password_hash, generate_password_hash


USERNAME_MIN = 1
USERNAME_MAX = 20
PASSWORD_MIN = 6
PASSWORD_MAX = 100

ITEM_TYPE = "user"

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.db.session.execute(db.text(sql), {"username":username})
    user = result.fetchone()

    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            print("login() USER PASSWORD OK")
            session["user"] = (username, user.id)
            return True
        else:
            return False
    else:
        return False
    

def register(username, password):
    try:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (item_type, username, password, created_at, is_admin, visible) VALUES (:item_type, :username, :password, NOW(), FALSE, TRUE)"
        db.db.session.execute(db.text(sql), {"item_type": ITEM_TYPE, "username":username, "password":hash_value})
        db.db.session.commit()
    except:
        return False
    
    return login(username, password)


def get_list():
    sql = "SELECT * FROM users ORDER BY username"
    result = db.db.session.execute(db.text(sql))

    return result.fetchall()


def logout():
    del session["user"]


def session_user_id():
    user = session.get("user", 0)
    return user[1] if user != 0 else None


def session_username():
    user = session.get("user", 0)
    return user[0] if user != 0 else None

def is_admin(id):
    sql = "SELECT id FROM users WHERE id=:id AND is_admin=TRUE"
    result = db.db.session.execute(db.text(sql), {"id":id})
    val = result.fetchone()

    if val:
        print("IS TRUE")
        return True
    return False


def get_username(id):
    sql = "SELECT username FROM users WHERE id=:id AND visible=TRUE"
    result = db.db.session.execute(db.text(sql), {"id":id})
    username = result.fetchone()
    return username[0]


def get_user_by_id(id):
    sql = "SELECT * FROM users WHERE id=:id AND visible=TRUE"
    result = db.db.session.execute(db.text(sql), {"id":id})
    user = result.fetchone()
    return user


def get_user_comments(id):
    sql = "SELECT * FROM comments WHERE user_id=:id AND visible=TRUE"
    result = db.db.session.execute(db.text(sql), {"id":id})
    comments = result.fetchall()
    return comments


def get_user_subforums(id):
    sql = "SELECT * FROM subforums WHERE user_id=:id AND visible=TRUE"
    result = db.db.session.execute(db.text(sql), {"id":id})
    subforums = result.fetchall()
    return subforums


def get_user_discussions(id):
    sql = "SELECT * FROM discussions WHERE user_id=:id AND visible=TRUE"
    result = db.db.session.execute(db.text(sql), {"id":id})
    discussions = result.fetchall()
    return discussions

def get_user_activity(id):
    
    tables = ["subforums", "discussions"]
    activity = []

    for table in tables:
        sql = f"SELECT * FROM {table} WHERE user_id=:id AND visible=TRUE"
        result = db.db.session.execute(db.text(sql), {"id":id})
        activity += result.fetchall()

    for item in activity:
        print(item)
        print()
        print()
        print()
        print()
        print()
        
    return activity

def does_username_exist(username):
    sql = "SELECT 1 FROM users WHERE username=:username"
    result = db.db.session.execute(db.text(sql), {"username":username})
    if result.fetchone():
        return True
    return False


def is_username_ok(username):
    if USERNAME_MAX >= len(username) >= USERNAME_MIN:
        if not helpers.contains_specials(username):
            print("USERNAME OK")
            return True
        print("USERNAME NOT OK")
    return False


def is_password_ok(password):
    if PASSWORD_MAX >= len(password) >= PASSWORD_MIN:
        if helpers.is_pass_secure(password):
            print("PASSWORD OK")
            return True
    print("PASSWORD NOT OK")
    return False


def search_by(query, sort_by, order_by):
    order = ""

    if sort_by == "created_at":
        order = " ORDER BY created_at"

    if order_by == "desc":
        order += " DESC"
    elif order_by == "asc":
        order += " ASC"

    sql = "SELECT * FROM users WHERE LOWER(username) LIKE LOWER(:query)" + order
    print(sql)

    result = db.db.session.execute(db.text(sql), {"query":"%"+query+"%"})

    return result.fetchall()


def delete(user_id1, user_id2):

    for table in ["comments", "discussions", "subforums"]:
        sql = f"UPDATE {table} SET visible=False WHERE user_id=:user_id1"

        db.db.session.execute(db.text(sql), {"user_id1":user_id1})
        db.db.session.commit()
    
    sql = f"UPDATE users SET visible=False WHERE id=:user_id1"
    db.db.session.execute(db.text(sql), {"user_id1":user_id1})
    db.db.session.commit()
    logout()