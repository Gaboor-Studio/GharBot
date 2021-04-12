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


def get_ghaar_user(conn, group_id, user_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM group_users WHERE group_id={group_id} and user_id={user_id};")
        # check numnber of rows affected
        return cur.fetchone()


def get_group_ghaar_users(conn, group_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM group_users WHERE group_id={group_id};")
        # check numnber of rows affected
        return cur.fetchall()


@commit
def insert_ghaar_user(conn, group_id, user_id):
    with conn.cursor() as cur:
        try:
            cur.execute(
                f"INSERT INTO group_users(group_id,user_id,count) VALUES ({group_id},{user_id},0);")
        except:
            print(f"Failed to add user({group_id},{user_id}) to database!")


@commit
def increase_ghaar_count(conn, group_id, user_id):
    with conn.cursor() as cur:
        cur.execute(
            f"UPDATE group_users SET count=count+1 WHERE group_id={group_id} and user_id={user_id};")


@commit
def delete_ghaar_user(conn, group_id, user_id):
    with conn.cursor() as cur:
        cur.execute(
            f"DELETE FROM group_users WHERE group_id={group_id} and user_id={user_id};")


def get_ghaar_message(conn, group_id, message_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM ghaar_messages WHERE group_id={group_id} and message_id={message_id};")
        return cur.fetchone()


def get_group_ghaar_messages(conn, group_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM ghaar_messages WHERE group_id={group_id};")
        return cur.fetchall()


@commit
def insert_ghaar_message(conn, group_id, message_id):
    with conn.cursor() as cur:
        try:
            cur.execute(
                f"INSERT INTO ghaar_messages(group_id,message_id) VALUES ({group_id},{message_id});")
        except:
            print(
                f"Failed to add message({group_id},{message_id}) to database!")


@commit
def delete_ghaar_message(conn, group_id, message_id):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM ghaar_messages WHERE group_id={group_id} and message_id={message_id};")


conn = connect('localhost', 'root', 'Amirparsa96', 'Ghaar')
cur = conn.cursor()
# insert_ghaar_message(conn, 2, 12833)
print(get_group_ghaar_users(conn, 2))
conn.close()
