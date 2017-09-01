from flask import Flask, render_template, redirect, request, session
from common import *
from datetime import datetime
import answer


# the main list.html page
@connection_handler
def question_index(cursor, criteria=None, order=None, limit=0):
    table = ordering(criteria, order, limit)
    header = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    return render_template('list.html', table=table, header=header, order=order, limit=limit)


# redirects to the question submitting page with a new id for the question
@connection_handler
def new_question(cursor):
    cursor.execute("""SELECT id
                      FROM question
                      ORDER BY id DESC
                      LIMIT 1;""")
    new_question_template = cursor.fetchall()
    return render_template("/form.html", id=new_question_template[0]["id"]+1, form_type="add_question")


@connection_handler
def add_question(cursor, new_question_data):
    new_question_data["submission_time"] = datetime.now().replace(microsecond=0)
    cursor.execute("INSERT INTO question \
                    (submission_time, vote_number, view_number, title, message, image) \
                    VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, {image}); \
                    ".format(image='NULL' if new_question_data["image"] == '' else '%(image)s'), new_question_data)
    cursor.execute("SELECT * FROM question ORDER BY id DESC LIMIT 1")
    new_question = cursor.fetchall()
    return redirect('/question/{}'.format(new_question[0]['id']))


@connection_handler
def display_question(cursor, question_id):
    cursor.execute("""UPDATE question
                      SET view_number = view_number + 1
                      WHERE id = %s;""", (question_id,))
    cursor.execute("""SELECT *
                      FROM question
                      WHERE id = %s
                      ORDER BY id;""", (question_id,))
    question_dict = cursor.fetchall()
    cursor.execute("""SELECT *
                      FROM answer
                    WHERE question_id = (%s);""", (question_id,))
    answer_list = cursor.fetchall()
    cursor.execute("""SELECT *
                      FROM comment
                      WHERE question_id = (%s);""", (question_id,))
    question_comments = cursor.fetchall()
    cursor.execute("""SELECT *
                      FROM comment
                      WHERE question_id IS NULL;""")
    answer_comments = cursor.fetchall()
    return render_template("display.html", question=question_dict[0], answers_list=answer_list,
                           question_comments=question_comments, answer_comments=answer_comments)


@connection_handler
def delete_question(cursor, question_id):
    cursor.execute("DELETE FROM question_tag WHERE question_id = %s;", (question_id,))
    cursor.execute("DELETE FROM comment WHERE question_id = %s;", (question_id,))
    cursor.execute("DELETE FROM question WHERE id = %s;", (question_id,))


@connection_handler
def delete_answers_for_question_id(cursor, question_id):
    cursor.execute("SELECT id FROM answer WHERE question_id = %s;", (question_id,))
    deleted_answers = cursor.fetchall()
    for answer_id in deleted_answers:
        cursor.execute("DELETE FROM comment WHERE answer_id = %(id)s;", answer_id)
        cursor.execute("DELETE FROM answer WHERE id = %(id)s;", answer_id)


# deleting a question by id
# deletes the answers for the deleted question too
# redirects to /list
def delete_question_with_answers(question_id):
    delete_answers_for_question_id(question_id)
    delete_question(question_id)
    return redirect('/list')


# editing a question by id
# replaces the question with the one gets from the form
# redirects to /list
@connection_handler
def edit_question(cursor, question_id, edited_question):
    cursor.execute("""UPDATE question
                      SET title = %s, message = %s, image = %s
                      WHERE id = %s
                      ;""", (edited_question["title"], edited_question["message"], edited_question["image"],
                             question_id))
    return redirect('/question/{}'.format(question_id))


@connection_handler
def question_for_edit(cursor, question_id):
    cursor.execute("""SELECT *
                      FROM question
                      WHERE id = %s
                      ;""", (question_id,))
    question_to_return = cursor.fetchall()
    question_to_return = question_to_return[0]
    return render_template("form.html", question=question_to_return, form_type="edit_question")


@connection_handler
def upvote_question(cursor, id_, vote):
    cursor.execute("UPDATE question \
                    SET vote_number = vote_number + {vote_var}, view_number = view_number -1 \
                    WHERE id = %s;".format(vote_var=1 if vote == "up" else -1), (id_,))
    return redirect("/question/{}".format(id_))


@connection_handler
def comment_question(cursor, question_id, message):
    cursor.execute("INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)"
                   "VALUES (%s, %s, %s, %s, %s);",
                   (question_id, None, message, datetime.now().replace(microsecond=0), 0))
    return redirect("/question/{}".format(question_id))
