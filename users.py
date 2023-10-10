import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.db.session.execute(db.text(sql), {"username":username})
    user = result.fetchone()

    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            print("USER PASSWORD OK")
            session["user"] = (username, user.id)
            return True
        else:
            return False
    else:
        return False
    
def register(username, password):
    try:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
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