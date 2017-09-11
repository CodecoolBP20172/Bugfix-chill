import psycopg2
import psycopg2.extras
from flask import Flask, render_template, redirect, request, session, url_for
from common import *
from datetime import datetime


@connection_handler
def register_user(cursor, user_name, password):
    cursor.execute("""SELECT name
                      FROM users;""")
    table = cursor.fetchall()
    existing_users = []
    for dictionary in table:
        existing_users.append(dictionary["name"])
    print(existing_users)
    if user_name in existing_users:
        return render_template("registration.html")
    else:
        cursor.execute("""INSERT INTO users (name, password, registration_time)
                          VALUES(%s, %s, %s);""", (user_name, password, datetime.now().replace(microsecond=0)))
        return redirect("/")
