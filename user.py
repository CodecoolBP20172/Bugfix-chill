from flask import Flask, render_template, redirect, request, session
from common import *


@connection_handler
def list_users(cursor):
    cursor.execute('SELECT username, password, registration_date, reputation \
                    FROM users;')
    user_dict = cursor.fetchall()
    user_headers = ["username", "password", "registration_date", "reputation"]
    return render_template('user_list.html', user_dict=user_dict, user_headers=user_headers)
