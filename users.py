import psycopg2
import psycopg2.extras
from flask import Flask, render_template, redirect, request, session, url_for
from common import *
from datetime import datetime


@connection_handler
def get_user_by_name(cursor, username):
    cursor.execute("""SELECT username, password, id
                      FROM users
                      WHERE username = %s;""", (username,))
    return cursor.fetchone()


@connection_handler
def register_user(cursor, user_name, password):
    cursor.execute("""SELECT username
                      FROM users;""")
    table = cursor.fetchall()
    existing_users = []
    for dictionary in table:
        existing_users.append(dictionary["username"])
    if user_name in existing_users:
        return False
    cursor.execute("""INSERT INTO users (username, password)
                      VALUES(%s, %s);""", (user_name, password))
    return True


@connection_handler
def list_users(cursor):
    cursor.execute('SELECT username, registration_date, reputation \
                    FROM users;')
    user_dict = cursor.fetchall()
    user_headers = ["username", "registration_date", "reputation"]
    return render_template('user_list.html', user_dict=user_dict, user_headers=user_headers)


@connection_handler
def get_user_stuffs(cursor, username):
    cursor.execute("""SELECT id, submission_time, view_number, vote_number, title
                   FROM question
                   WHERE question.username = %(user)s;""", {"user": username})
    users_questions = cursor.fetchall()
    cursor.execute("""SELECT answer.submission_time, answer.vote_number, answer.message, question.title, answer.question_id
                   FROM answer
                   JOIN question
                   ON (answer.question_id = question.id)
                   WHERE answer.username = %(user)s;""", {"user": username})
    users_answers = cursor.fetchall()
    cursor.execute("""SELECT comment.id, comment.submission_time, comment.message, question.id AS question_id, answer.id AS answer_id, answer.question_id AS other_question_id
                   FROM comment
                   LEFT JOIN question
                   ON (comment.question_id = question.id)
                   LEFT JOIN answer
                   ON (comment.answer_id = answer.id)
                   WHERE comment.username = %(user)s;""", {"user": username})
    users_comments = cursor.fetchall()
    return users_questions, users_answers, users_comments
