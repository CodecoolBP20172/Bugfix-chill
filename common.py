from config import Config
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, redirect, request, session, url_for


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
    cursor.execute("SELECT question_id FROM comment WHERE id= (%s);", (comment_id,))
    question_id = cursor.fetchall()
    print("ID: ", question_id)
    if (question_id[0]["question_id"]) is None:
        print("HI!!!!!!!!!!!!!!!!!")
        cursor.execute("SELECT answer_id FROM comment WHERE id = (%s);", (comment_id,))
        answer_id = cursor.fetchall()
        cursor.execute("SELECT question_id FROM answer WHERE id = (%s);", (answer_id[0]["answer_id"],))
        question_id = cursor.fetchall()
    question_id = question_id[0]["question_id"]
    cursor.execute("DELETE FROM comment WHERE id = (%s);", (comment_id,))
    return redirect("/question/{}".format(question_id))


def url_validation(criteria, order):
    valid_criteria = ['submission_time', 'view_number', 'vote_number']
    valid_order = ['ASC', 'DESC']
    if criteria and order and (criteria in valid_criteria and order in valid_order):
        return True
    else:
        return False
