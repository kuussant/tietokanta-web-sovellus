import db

import users


def get_list():
    sql = "SELECT S.id, S.title, S.followers, S.created_at, S.user_id, (SELECT username FROM users WHERE S.user_id = id) AS username FROM subforums S ORDER BY S.created_at"
    result = db.db.session.execute(db.text(sql))
    return result.fetchall()


def get_sub(id):
    sql = "SELECT title, content, followers, created_at, user_id FROM subforums WHERE id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})
    return result.fetchone()


def create_new_sub(title, content, user_id):
    sql = "INSERT INTO subforums (title, content, followers, user_id, created_at) VALUES (:title, :content, :followers, :user_id, NOW())"
    db.db.session.execute(db.text(sql), {"title":title, "content":content, "followers":0, "user_id":user_id})
    db.db.session.commit()