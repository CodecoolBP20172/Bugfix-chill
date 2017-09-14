from flask import Flask, render_template, redirect, request, session, url_for
from datetime import datetime
from common import *


@connection_handler
def post_an_answer(cursor, question_id, message, image):
    cursor.execute("INSERT INTO answer (submission_time, vote_number, question_id, message, image, username) VALUES "
                   "(%s, %s, %s, %s, %s, %s);", (datetime.now().replace(microsecond=0), 0, question_id, message,
                                                 image, session["username"]))
    return redirect("/question/{}".format(question_id))


@connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""SELECT question_id
                      FROM answer
                      WHERE id = (%s);""", (answer_id,))
    question_id = cursor.fetchall()
    cursor.execute("""DELETE FROM answer
                      WHERE id = (%s);""", (answer_id,))
    cursor.execute("""UPDATE question
                      SET view_number = view_number - 1
                      WHERE id = (%s);""", (question_id[0]["question_id"],))


@connection_handler
def upvote(cursor, id_, question_id, vote, username):
    cursor.execute("""SELECT vote_number
                      FROM answer
                      WHERE id = (%s);""", (id_,))
    current_vote = cursor.fetchall()
    current_vote = current_vote[0]
    current_vote = current_vote["vote_number"]
    cursor.execute("""UPDATE users
                      SET reputation = reputation + {rep}
                      WHERE username = %s;""".format(rep=10 if vote == "up" else -2), (username,))
    cursor.execute("""UPDATE answer
                      SET vote_number = vote_number + {vote}
                      WHERE username = %s;""".format(vote=1 if vote == "up" else -1), (username,))
    cursor.execute("""UPDATE question
                      SET view_number = view_number - 1
                      WHERE id = (%s);""", (question_id,))
    return redirect("/question/{}".format(question_id))


@connection_handler
def comment_answer(cursor, answer_id, message):
    cursor.execute("""INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, username)
                      VALUES (%s, %s, %s, %s, %s, %s);""",
                   (None, answer_id, message, datetime.now().replace(microsecond=0), 0, session["username"]),)
    cursor.execute("""SELECT question_id
                      FROM answer
                      WHERE id=%s;""", (answer_id,))
    question_id = cursor.fetchall()
    question_id = question_id[0]["question_id"]
    return redirect("/question/{}".format(question_id))


@connection_handler
def edit_answer(cursor, answer_id):
    cursor.execute("""SELECT *
                      FROM answer
                      WHERE id = %s;""", (answer_id,))
    answer = cursor.fetchone()
    return render_template("form.html", form_type="edit_answer", answer=answer)


@connection_handler
def edited_answer(cursor, message, image, answer_id, question_id):
    cursor.execute("""UPDATE answer
                      SET message = %s, image = %s
                      WHERE id = %s;""", (message, image, answer_id))
    return redirect("/question/{}".format(question_id))
