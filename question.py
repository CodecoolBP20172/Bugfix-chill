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


# answer_list contains all the answers to a particular question
# answer_comments contains all comments connecting to the question's answers
# returns answers_comment_count that is a dictionary where the keys are the answer_id
# and the value is the number of comments connecting to that answer
def get_answer_comment_len(answer_list, answer_comments):
    if len(answer_list) == 0:
        return 0
    comment_counter = 0
    answer_id_list = list()
    answers_comment_count = dict()
    for answer in answer_list:
        answer_id_list.append(answer["id"])
        answers_comment_count.update({answer["id"]: 0})
    for comment in answer_comments:
        if comment["answer_id"] in answer_id_list:
            answers_comment_count[comment["answer_id"]] += 1
    return answers_comment_count


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
                      WHERE question_id = (%s)
                      ORDER BY vote_number DESC;""", (question_id,))
    answer_list = cursor.fetchall()
    cursor.execute("""SELECT *
                      FROM comment
                      WHERE question_id = (%s);""", (question_id,))
    question_comments = cursor.fetchall()
    cursor.execute("""SELECT *
                      FROM comment
                      WHERE answer_id IN (SELECT id FROM answer WHERE question_id = (%s));""", (question_id,))
    answer_comments = cursor.fetchall()
    answer_comment_count = get_answer_comment_len(answer_list, answer_comments)
    get_reputation = cursor.execute("""SELECT reputation
                                       FROM users
                                       WHERE username IN
                                       (SELECT username FROM question WHERE id = (%s));""", question_id)
    reputation = cursor.fetchall()
    print(reputation)
    return render_template("display.html", question=question_dict[0], answers_list=answer_list,
                           question_comments=question_comments, answer_comments=answer_comments,
                           answer_comment_count=answer_comment_count, reputation=reputation[0])


# deleting a question by id
# deletes the answers for the deleted question too
# redirects to /list
def delete_question_with_answers(question_id):
    cursor.execute("DELETE FROM question WHERE id = %s;", (question_id,))
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
def upvote_question(cursor, id_, vote, username):
    cursor.execute("UPDATE question \
                    SET vote_number = vote_number + {vote_var}, view_number = view_number -1 \
                    WHERE id = %s;".format(vote_var=1 if vote == "up" else -1), (id_,))
    cursor.execute("""UPDATE users
                      SET reputation = reputation + {rep}
                      WHERE username = %s;""".format(rep=15 if vote == "up" else -2), (username,))
    return redirect("/question/{}".format(id_))


@connection_handler
def comment_question(cursor, question_id, message):
    cursor.execute("INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)"
                   "VALUES (%s, %s, %s, %s, %s);",
                   (question_id, None, message, datetime.now().replace(microsecond=0), 0))
    return redirect("/question/{}".format(question_id))
