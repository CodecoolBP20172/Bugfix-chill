import psycopg2
import psycopg2.extras
from flask import Flask, render_template, redirect, request, session, url_for
from common import *
from datetime import datetime


@connection_handler
def login_to_page(cursor, username, password):
    cursor.execute("""SELECT username, password
                      FROM users
                      WHERE username = %s;""", (username,))
    table = cursor.fetchall()
    if table:
        if table[0]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
    return redirect("login.html")
