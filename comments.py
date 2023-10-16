import db

import users

def get_list_by_id(id):
    sql = "SELECT * FROM comments WHERE discussion_id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})
    return result.fetchall()


def get_comment(id):
    sql = "SELECT title, content, followers, created_at FROM comments WHERE id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})
    return result.fetchone()


def create_new_comment(content, disc_id, user_id):
    sql = "INSERT INTO comments (content, discussion_id, user_id, created_at) VALUES (:content, :discussion_id, :user_id, NOW())"
    db.db.session.execute(db.text(sql), {"content":content, "discussion_id":disc_id, "user_id":user_id})
    db.db.session.commit()