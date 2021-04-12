import pymysql
import traceback


class ForwardedMessage:

    def __init__(self, group_id, message_id, caption, image_hash, video_hash):
        self.group_id = group_id
        self.message_id = message_id
        self.caption = caption
        self.image_hash = image_hash
        self.video_hash = video_hash


def connect(host, user, password, db):
    conn = pymysql.connect(host=host, user=user, passwd=password, db=db)
    return conn


'''Fetch ghaar user from db'''


def get_ghaar_user(conn, group_id, user_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM group_users WHERE group_id={group_id} and user_id={user_id};")
        return cur.fetchone()


'''Fetch ghaar user from db by id'''


def get_ghaar_user_by_id(conn, user_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM group_users WHERE user_id={user_id};")
        return cur.fetchall()


'''Fetch group ghaar users from db'''


def get_group_ghaar_users(conn, group_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM group_users WHERE group_id={group_id};")
        return cur.fetchall()


'''Create a new ghaar user in group'''


def insert_ghaar_user(conn, group_id, user_id):
    with conn.cursor() as cur:
        try:
            cur.execute(
                f"INSERT INTO group_users(group_id,user_id,count) VALUES ({group_id},{user_id},0);")
            conn.commit()
        except:
            print(f"Failed to add user({group_id},{user_id}) to database!")
            traceback.print_exc()


'''Increases ghaar count for a user in group. If user does not exist in db, it creates the user automatically.'''


def increase_ghaar_count(conn, group_id, user_id):
    if get_ghaar_user(conn, group_id, user_id) == None:
        insert_ghaar_user(conn, group_id, user_id)
    with conn.cursor() as cur:
        cur.execute(
            f"UPDATE group_users SET count=count+1 WHERE group_id={group_id} and user_id={user_id};")
        conn.commit()


'''Deletes a ghaar user from db.'''


def delete_ghaar_user(conn, group_id, user_id):
    with conn.cursor() as cur:
        cur.execute(
            f"DELETE FROM group_users WHERE group_id={group_id} and user_id={user_id};")
        conn.commit()


'''Fetchs a ghaar message in group.'''


def get_ghaar_message(conn, group_id, message_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM ghaar_messages WHERE group_id={group_id} and message_id={message_id};")
        return cur.fetchone()
        conn.commit()


'''Fatchs all of ghaar messages in group.'''


def get_ghaar_messages_by_group_id(conn, group_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM ghaar_messages WHERE group_id={group_id};")
        return cur.fetchall()


'''Adds a new ghaar message in group.'''


def insert_ghaar_message(conn, group_id, message_id):
    with conn.cursor() as cur:
        try:
            cur.execute(
                f"INSERT INTO ghaar_messages(group_id,message_id) VALUES ({group_id},{message_id});")
            conn.commit()
        except:
            print(
                f"Failed to add message({group_id},{message_id}) to database!")
            traceback.print_exc()


'''Deletes a ghaar message from group.'''


def delete_ghaar_message(conn, group_id, message_id):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM ghaar_messages WHERE group_id={group_id} and message_id={message_id};")
        conn.commit()


'''Fetches a forwarded message in group'''


def get_forwarded_message(conn, group_id, message_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM messages WHERE group_id={group_id} and message_id={message_id};")
        return cur.fetchone()
        conn.commit()


'''Fetches all forwarded messages by group id'''


def get_all_forwarded_messages(conn, group_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM ghaar_messages WHERE group_id={group_id};")
        return cur.fetchall()


'''Adds a forwarded message to db'''


def insert_forwarded_message_by_data(conn, group_id, message_id, caption, image_hash, video_hash):
    with conn.cursor() as cur:
        try:
            cur.execute(f"INSERT INTO messages(group_id,message_id,caption,image_hash,video_hash) VALUES \
                ({group_id},{message_id},'{caption}','{image_hash}','{video_hash}')")
            conn.commit()
        except:
            print(
                f"Failed to add forwarded message ({group_id},{message_id},{caption},{image_hash},{video_hash})")
            traceback.print_exc()


'''Adds a forwarded message to db'''


def insert_forwarded_message(conn, message: ForwardedMessage):
    insert_forwarded_message_by_data(conn, message.group_id, message.message_id,
                                     message.caption, message.image_hash, message.video_hash)


'''Deletes forwarded message from db'''


def delete_forwarded_message(conn, group_id, message_id):
    with conn.cursor() as cur:
        cur.execute(
            f"DELETE FROM messages WHERE group_id={group_id} and message_id={message_id};")
    conn.commit()


'''deletes forwarded message by group_id'''


def delete_forwarded_messages_by_group_id(conn, group_id):
    with conn.cursor() as cur:
        cur.execute(
            f"DELETE FROM messages WHERE group_id={group_id};")
    conn.commit()
