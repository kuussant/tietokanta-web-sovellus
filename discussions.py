import db

import users


ITEM_TYPE = "discussion"


def get_list_by_sub_id(id):
    sql = "SELECT D.id, D.title, D.content, D.created_at, D.subforum_id, D.user_id, (SELECT username FROM users WHERE D.user_id=id) AS username FROM discussions D WHERE D.subforum_id=:id ORDER BY D.created_at DESC"
    result = db.db.session.execute(db.text(sql), {"id":id})

    return result.fetchall()


def get_list_by_user_id(id):
    sql = "SELECT * FROM discussions WHERE user_id=:id ORDER BY created_at DESC"
    result = db.db.session.execute(db.text(sql), {"id":id})

    return result.fetchall()


def get_discussion(id):
    sql = "SELECT * FROM discussions WHERE id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})

    return result.fetchone()


def create_new_discussion(title, content, subforum_id, user_id):
    sql = "INSERT INTO discussions (item_type, title, content, subforum_id, user_id, created_at) VALUES (:item_type, :title, :content, :subforum_id, :user_id, NOW())"
    db.db.session.execute(db.text(sql), {"item_type":ITEM_TYPE, "title":title, "content":content, "subforum_id":subforum_id, "user_id":user_id})

    db.db.session.commit()