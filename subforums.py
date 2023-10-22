import db


ITEM_TYPE = "subforum"


def get_list():
    sql = "SELECT *, (SELECT username FROM users WHERE S.user_id = id) AS username FROM subforums S WHERE S.visible=TRUE ORDER BY S.created_at DESC"
    result = db.db.session.execute(db.text(sql))
    return result.fetchall()


def get_list_by_user_id(id):
    sql = "SELECT * FROM subforums WHERE user_id=:id AND visible=TRUE ORDER BY created_at DESC"
    result = db.db.session.execute(db.text(sql), {"id":id})
    return result.fetchall()


def get_sub(id):
    sql = "SELECT * FROM subforums WHERE id=:id AND visible=TRUE"
    result = db.db.session.execute(db.text(sql), {"id":id})
    return result.fetchone()


def create_new_sub(title, content, user_id):
    sql = "INSERT INTO subforums (item_type, title, content, followers, user_id, created_at, visible) VALUES (:item_type, :title, :content, :followers, :user_id, NOW(), TRUE)"
    db.db.session.execute(db.text(sql), {"item_type":ITEM_TYPE, "title":title, "content":content, "followers":0, "user_id":user_id})
    db.db.session.commit()


def search_by(query, order_by):
    order = ""

    if order_by == "newest":
        order = " ORDER BY created_at DESC"
    elif order_by == "oldest":
        order = " ORDER BY created_at ASC"

    sql = "SELECT * FROM subforums WHERE LOWER(title) LIKE LOWER(:query)" + order
    print(sql)

    result = db.db.session.execute(db.text(sql), {"query":"%"+query+"%"})

    return result.fetchall()


def follow(sub_id, user_id):
    sql = ""

    if does_user_follow_sub(sub_id, user_id, True):
        sql = "UPDATE follows_subforum SET visible=TRUE WHERE subforum_id=:sub_id AND user_id=:user_id"
    else:
        sql = "INSERT INTO follows_subforum (subforum_id, user_id, visible) VALUES (:sub_id, :user_id, TRUE)"

    db.db.session.execute(db.text(sql), {"sub_id":sub_id, "user_id":user_id})
    db.db.session.commit()


def unfollow(sub_id, user_id):
    sql = "UPDATE follows_subforum SET visible=FALSE WHERE subforum_id=:sub_id AND user_id=:user_id"
    db.db.session.execute(db.text(sql), {"sub_id":sub_id, "user_id":user_id})
    db.db.session.commit()


def get_followers(sub_id):
    sql = "SELECT * FROM follows_subforum WHERE subforum_id=:sub_id AND visible=TRUE"
    result = db.db.session.execute(db.text(sql), {"sub_id":sub_id})
    
    return result.fetchall()


def get_user_followed_subs(user_id):
    sql = "SELECT S.* FROM follows_subforum F, subforums S WHERE F.user_id=:user_id AND F.subforum_id=S.id"
    result = db.db.session.execute(db.text(sql), {"user_id":user_id})
    
    return result.fetchall()


def does_user_follow_sub(sub_id, user_id, visible_false):
    vis = ""

    if visible_false == 1:
        vis = "visible=FALSE"
    else:
        vis = "visible=TRUE"

    sql = "SELECT 1 FROM follows_subforum WHERE subforum_id=:sub_id AND user_id=:user_id AND " + vis
    result = db.db.session.execute(db.text(sql), {"sub_id":sub_id, "user_id":user_id})
    
    if result.fetchone():
        return True
    
    return False


def update_contents(id, title, content):
    sql = "UPDATE subforums SET title=:title, content=:content WHERE id=:id AND visible=TRUE"
    db.db.session.execute(db.text(sql), {"id":id, "title":title, "content":content})
    db.db.session.commit()


def delete(sub_id, user_id):
    sql = f"UPDATE subforums SET visible=False WHERE id=:sub_id AND user_id=:user_id OR (SELECT is_admin FROM users WHERE id=:user_id)"
    db.db.session.execute(db.text(sql), {"user_id":user_id, "sub_id":sub_id})
    db.db.session.commit()