from flask import Flask, render_template, redirect, request, session, url_for
from datetime import datetime
from common import *


@connection_handler
def post_an_answer(cursor, question_id, message, image):
    cursor.execute("INSERT INTO answer (submission_time, vote_number, question_id, message, image) VALUES "
                   "(%s, %s, %s, %s, %s);", (datetime.now(), 0, question_id, message, image))
    return redirect("/question/{}".format(question_id))


@connection_handler
def delete_answer(cursor, answer_id, question_id):
    cursor.execute("DELETE FROM comment WHERE answer_id = (%s);", (answer_id))
    cursor.execute("DELETE FROM answer WHERE id = (%s);", (answer_id))


@connection_handler
def upvote(cursor, id_, question_id, vote):
    cursor.execute("SELECT vote_number FROM answer WHERE id = (%s);", (id_))
    current_vote = cursor.fetchall()
    current_vote = current_vote[0]
    current_vote = current_vote["vote_number"]
    if vote == "up":
        current_vote += 1
        cursor.execute("UPDATE answer SET vote_number = (%s) WHERE id = (%s);", (current_vote, id_))
    else:
        current_vote -= 1
        cursor.execute("UPDATE answer SET vote_number = (%s) WHERE id = (%s);", (current_vote, id_))
    return redirect("/question/{}".format(question_id))
