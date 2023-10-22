import db


ITEM_TYPE = "discussion"

def get_list():
    sql = "SELECT *, (SELECT username FROM users WHERE D.user_id = id) AS username FROM discussions D WHERE D.visible=TRUE ORDER BY D.created_at DESC"
    result = db.db.session.execute(db.text(sql))
    return result.fetchall()

def get_list_by_sub_id(id):
    sql = "SELECT *, (SELECT username FROM users WHERE D.user_id=id) AS username FROM discussions D WHERE D.subforum_id=:id AND D.visible=TRUE ORDER BY D.created_at DESC"
    result = db.db.session.execute(db.text(sql), {"id":id})

    return result.fetchall()


def get_list_by_user_id(id):
    sql = "SELECT * FROM discussions WHERE user_id=:id AND visible=TRUE ORDER BY created_at DESC"
    result = db.db.session.execute(db.text(sql), {"id":id})

    return result.fetchall()


def get_discussion(id):
    sql = "SELECT * FROM discussions WHERE id=:id AND visible=TRUE"
    result = db.db.session.execute(db.text(sql), {"id":id})

    return result.fetchone()


def create_new_discussion(title, content, subforum_id, user_id):
    sql = "INSERT INTO discussions (item_type, title, content, subforum_id, user_id, created_at, visible) VALUES (:item_type, :title, :content, :subforum_id, :user_id, NOW(), TRUE)"
    db.db.session.execute(db.text(sql), {"item_type":ITEM_TYPE, "title":title, "content":content, "subforum_id":subforum_id, "user_id":user_id})

    db.db.session.commit()


def search_by(query, order_by):
    order = ""

    if order_by == "newest":
        order = " ORDER BY created_at DESC"
    elif order_by == "oldest":
        order = " ORDER BY created_at ASC"

    sql = "SELECT * FROM discussions WHERE LOWER(title) LIKE LOWER(:query)" + order
    print(sql)

    result = db.db.session.execute(db.text(sql), {"query":"%"+query+"%"})

    return result.fetchall()


def delete(disc_id, user_id):
    sql = f"UPDATE discussions SET visible=False WHERE id=:disc_id AND user_id=:user_id OR (SELECT is_admin FROM users WHERE id=:user_id)"
    db.db.session.execute(db.text(sql), {"user_id":user_id, "disc_id":disc_id})
    db.db.session.commit()