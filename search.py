import db

NEWEST = "newest"
OLDEST = "oldest"
MOST_FOLLOWS = "most_follows"

def search(table, query, order_by):
    order_by = ""

    if order_by == NEWEST:
        order_by = "created_at DESC"
    
    elif order_by == OLDEST:
        order_by == "created_at ASC"
    
    elif order_by == MOST_FOLLOWS:
        order_by = "(SELECT * FROM )"

    sql = f"SELECT * FROM {table} WHERE title LIKE :query ORDER BY {order_by}"
    result = db.session.execute(sql, {"query":"%"+query+"%"})

    return result.fetchall()