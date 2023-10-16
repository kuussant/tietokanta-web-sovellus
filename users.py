import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

USERNAME_MIN = 3
USERNAME_MAX = 20
PASSWORD_MIN = 6
PASSWORD_MAX = 30

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
        sql = "INSERT INTO users (username, password, created_at) VALUES (:username, :password, NOW())"
        db.db.session.execute(db.text(sql), {"username":username, "password":hash_value})
        db.db.session.commit()
    except:
        return False
    
    return login(username, password)

def profile():
    pass

def logout():
    del session["user"]

def session_user_id():
    user = session.get("user", 0)
    return user[1] if user != 0 else None

def session_username():
    user = session.get("user", 0)
    return user[0] if user != 0 else None

def get_username(id):
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})
    username = result.fetchone()
    return username[0]

def get_user_by_id(id):
    sql = "SELECT * FROM users WHERE id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})
    user = result.fetchone()
    return user

def get_user_comments(id):
    sql = "SELECT * FROM comments WHERE user_id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})
    comments = result.fetchall()
    return comments

def get_user_subforums(id):
    sql = "SELECT * FROM subforums WHERE user_id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})
    subforums = result.fetchall()
    return subforums

def get_user_discussions(id):
    sql = "SELECT * FROM discussions WHERE user_id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})
    discussions = result.fetchall()
    return discussions

def does_username_exist(username):
    sql = "SELECT 1 FROM users WHERE username=:username"
    result = db.db.session.execute(db.text(sql), {"username":username})
    if result.fetchone():
        print("yoooooo")
        return True
    return False

def is_username_ok(username):
    if USERNAME_MAX >= len(username) >= USERNAME_MIN:
        return True
    return False

def is_password_ok(password):
    if PASSWORD_MAX >= len(password) >= PASSWORD_MIN:
        return True
    return False