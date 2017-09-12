import psycopg2
import psycopg2.extras
from flask import Flask, render_template, redirect, request, session, url_for
from common import *
from datetime import datetime


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
    cursor.execute("""INSERT INTO users (username, password, registration_date)
                      VALUES(%s, %s, %s);""", (user_name, password, datetime.now().replace(microsecond=0)))
    return True
