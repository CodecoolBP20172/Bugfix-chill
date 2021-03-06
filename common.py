from config import Config
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, redirect, request, session, url_for
import bcrypt


def open_database():
    try:
        connection_string = Config.DB_CONNECTION_STR
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print(exception)
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a dict cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value
    return wrapper


@connection_handler
def ordering(cursor, criteria, order, limit):
    if criteria and order:
        order_dict = {'criteria': criteria, 'order': order, 'limit': limit}
        if limit:
            cursor.execute("SELECT * FROM question WHERE id IN \
                        (SELECT id FROM question ORDER BY id DESC LIMIT 5) \
                        ORDER BY {criteria} {order}; \
                        ".format(criteria=order_dict['criteria'], order=order_dict['order'], limit=order_dict['limit']))
        else:
            cursor.execute("SELECT * FROM question ORDER BY {criteria} {order}; \
                        ".format(criteria=order_dict['criteria'], order=order_dict['order']))
    else:
        cursor.execute("SELECT * FROM question ORDER BY id DESC {limit_val}; \
        ".format(limit_val='' if limit == 0 else " LIMIT 5"))
    table = cursor.fetchall()
    return table


@connection_handler
def remove_comment(cursor, comment_id):
    question_id = get_question_id(comment_id)
    cursor.execute("""DELETE FROM comment
                      WHERE id = (%s);""", (comment_id,))
    return redirect("/question/{}".format(question_id))


def url_validation(criteria, order):
    valid_criteria = ['submission_time', 'view_number', 'vote_number']
    valid_order = ['ASC', 'DESC']
    if criteria and order and (criteria in valid_criteria and order in valid_order):
        return True
    else:
        return False


@connection_handler
def edit_comment(cursor, comment_id):
    cursor.execute("""SELECT *
                      FROM comment
                      WHERE id = (%s);""", (comment_id,))
    comment_data = cursor.fetchall()
    return render_template("form.html", comment_id=comment_id, comment_data=comment_data[0], form_type="edit_comment")


@connection_handler
def submit_comment_edited(cursor, comment_id, message):
    question_id = get_question_id(comment_id)
    cursor.execute("""UPDATE comment
                      SET message = (%s), edited_count = edited_count +1
                      WHERE id = (%s);""", (message, comment_id))
    return redirect("/question/{}".format(question_id))


@connection_handler
def get_question_id(cursor, comment_id):
    cursor.execute("""SELECT question_id
                      FROM comment
                      WHERE id= (%s);""", (comment_id,))
    question_id = cursor.fetchall()
    if (question_id[0]["question_id"]) is None:
        cursor.execute("""SELECT answer_id
                          FROM comment
                          WHERE id = (%s);""", (comment_id,))
        answer_id = cursor.fetchall()
        cursor.execute("""SELECT question_id
                          FROM answer
                          WHERE id = (%s);""", (answer_id[0]["answer_id"],))
        question_id = cursor.fetchall()
    question_id = question_id[0]["question_id"]
    return question_id


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def check_password(plain_text_password, hashed_text_password):
    hashed_bytes_password = hashed_text_password.encode("utf-8")
    # Check hased password. Useing bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
