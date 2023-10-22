import db

ITEM_TYPE = "comment"


def get_list_by_id(id):
    sql = "SELECT * FROM comments WHERE discussion_id=:id AND visible=TRUE ORDER BY created_at DESC"
    result = db.db.session.execute(db.text(sql), {"id":id})
    return result.fetchall()


def get_list_by_user_id(id):
    sql = "SELECT * FROM comments WHERE user_id=:id AND visible=TRUE ORDER BY created_at DESC"
    result = db.db.session.execute(db.text(sql), {"id":id})

    return result.fetchall()


def get_comment(id):
    sql = "SELECT * FROM comments WHERE id=:id AND visible=TRUE"
    result = db.db.session.execute(db.text(sql), {"id":id})
    return result.fetchone()


def create_new_comment(content, disc_id, user_id):
    sql = "INSERT INTO comments (item_type, content, discussion_id, user_id, created_at, visible) VALUES (:item_type, :content, :discussion_id, :user_id, NOW(), TRUE)"
    db.db.session.execute(db.text(sql), {"item_type":ITEM_TYPE, "content":content, "discussion_id":disc_id, "user_id":user_id})
    db.db.session.commit()


def delete(comment_id, user_id):
    sql = f"UPDATE comments SET visible=False WHERE id=:comment_id AND user_id=:user_id OR (SELECT is_admin FROM users WHERE id=:user_id)"
    db.db.session.execute(db.text(sql), {"user_id":user_id, "comment_id":comment_id})
    db.db.session.commit()