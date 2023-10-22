import db


ITEM_TYPE = "subforum"


def get_list():
    sql = "SELECT *, (SELECT username FROM users WHERE S.user_id = id) AS username FROM subforums S ORDER BY S.created_at DESC"
    result = db.db.session.execute(db.text(sql))
    return result.fetchall()


def get_list_by_user_id(id):
    sql = "SELECT * FROM subforums WHERE user_id=:id ORDER BY created_at DESC"
    result = db.db.session.execute(db.text(sql), {"id":id})
    return result.fetchall()


def get_sub(id):
    sql = "SELECT * FROM subforums WHERE id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})
    return result.fetchone()


def create_new_sub(title, content, user_id):
    sql = "INSERT INTO subforums (item_type, title, content, followers, user_id, created_at) VALUES (:item_type, :title, :content, :followers, :user_id, NOW())"
    db.db.session.execute(db.text(sql), {"item_type":ITEM_TYPE, "title":title, "content":content, "followers":0, "user_id":user_id})
    db.db.session.commit()