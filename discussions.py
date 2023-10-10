import db
import users

def get_list_by_sub_id(id):
    sql = "SELECT * FROM discussions WHERE subforum_id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})
    return result.fetchall()

def get_discussion(id):
    sql = "SELECT title, content, created_at FROM discussions WHERE id=:id"
    result = db.db.session.execute(db.text(sql), {"id":id})
    return result.fetchone()

def create_new_discussion(title, content, subforum_id, user_id):
    sql = "INSERT INTO discussions (title, content, subforum_id, user_id, created_at) VALUES (:title, :content, :subforum_id, :user_id, NOW())"
    db.db.session.execute(db.text(sql), {"title":title, "content":content, "subforum_id":subforum_id, "user_id":user_id})
    db.db.session.commit()