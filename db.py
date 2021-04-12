import pymysql


def connect(host, user, password, db):
    conn = pymysql.connect(host=host, user=user, passwd=password, db=db)
    return conn


def commit(func):
    def wrapper_func(conn, group_id, user_id):
        func(conn, group_id, user_id)
        conn.commit()
        conn.cursor().close()
    return wrapper_func


def get(conn, group_id, user_id):
    with conn.cursor() as cur:
        rows_affected = cur.execute(
            f"SELECT * from group_users WHERE group_id={group_id} and user_id={user_id};")
        # check numnber of rows affected
        return cur.fetchone()


@commit
def insert(conn, group_id, user_id):
    with conn.cursor() as cur:
        rows_affected = cur.execute(
            f"SELECT * from group_users WHERE group_id={group_id} and user_id={user_id};")
        # check numnber of rows affected
        if rows_affected == 0:
            rows_affected = cur.execute(
                f"INSERT INTO group_users(group_id,user_id,count) VALUES ({group_id},{user_id},0);")


@commit
def increase(conn, group_id, user_id):
    with conn.cursor() as cur:
        rows_affected = cur.execute(
            f"Select * from group_users WHERE group_id={group_id} and user_id={user_id};")
        # check numnber of rows affected
        if rows_affected != 0:
            (group, user, count) = cur.fetchone()
            rows_affected = cur.execute(
                f"UPDATE group_users SET count={count+1} WHERE group_id={group_id} and user_id={user_id};")


@commit
def delete(conn, group_id, user_id):
    with conn.cursor() as cur:
        rows_affected = cur.execute(
            f"DELETE from group_users WHERE group_id={group_id} and user_id={user_id};")


# conn = connect('localhost', 'root', 'Amirparsa96', 'Ghaar')
# cur = conn.cursor()
# delete(conn, 3, 4)

# conn.close()
