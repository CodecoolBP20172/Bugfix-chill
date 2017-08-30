from flask import Flask, render_template, redirect, request, session
from common import *
import datetime


# the main list.html page
@connection_handler
def question_index(cursor, criteria, order):
    cursor.execute("SELECT * FROM question;")
    table = cursor.fetchall()
    # table = ordering(table, criteria, order)
    header = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    return render_template('list.html', table=table, header=header, order=order)


@connection_handler
def delete_question(cursor, question_id):
    cursor.execute("DELETE FROM question_tag WHERE question_id = %s RETURNING *;", question_id)
    deleted_tag = cursor.fetchall()
    cursor.execute("DELETE FROM question WHERE id = %s RETURNING *;", question_id)
    deleted_question = cursor.fetchall()
    print (deleted_tag, deleted_question)


@connection_handler
def delete_answers_for_question_id(cursor, question_id):
    cursor.execute("DELETE FROM answer WHERE question_id = %s RETURNING *;", question_id)
    deleted_answers = cursor.fetchall()
    for answer in deleted_answers:
        print (answer)


# deleting a question by id
# deletes the answers for the deleted question too
# redirects to /list
def delete_question_with_answers(question_id):
    delete_question(question_id)
    delete_answers_for_question_id(question_id)
    return redirect('/list')


# editing a question by id
# replaces the question with the one gets from the form
# redirects to /list
@connection_handler
def edit_question(cursor, question_id, edited_question):
    if question_id == edited_question['id']:
        cursor.execute("""UPDATE question
                          SET title = %(title)s, message = %(message)s, image = %(image)s
                          WHERE iD = %(id)s RETURNING *;""", edited_question)
    return redirect('/')


@connection_handler
def question_for_edit(question_id):
    table = read_from_csv('data/question.csv')
    question_to_return = None
    for question in table:
        if question["ID"] == question_id:
            question_to_return = question
            break
    return render_template("form.html", question=question_to_return, form_type="edit_question")


# redirects to the question submitting page with a new id for the question
@connection_handler
def new_question():
    table = read_from_csv('data/question.csv')
    new_id = id_generation(table)
    return render_template("/form.html", id=new_id, form_type="add_question")


@connection_handler
def question_to_display_format(question):
    tmp_dict = dict(question)
    # tmp_dict["submission_time"] = date_from_timestamp(tmp_dict["submission_time"])
    # tmp_dict["title"] = tmp_dict["title"].replace('\\n', '<br>')
    # tmp_dict["message"] = tmp_dict["message"].replace('\r\n', '<br>')
    return tmp_dict


@connection_handler
def answer_to_display_format(answer):
    answer["message"] = answer["message"].replace('\\n', '<br>')
    return answer


@connection_handler
def display_question(question_id):
    table = read_from_csv('data/question.csv')
    answers_list = list()
    question_to_display = None
    for question in table:
        if question["ID"] == question_id:
            view_counter = int(question["view_number"]) + 1
            question["view_number"] = str(view_counter)
            question_to_display = question_to_display_format(question)
            break
    answer_table = read_from_csv('data/answer.csv')
    for answer in answer_table:
        answer["submission_time"] = date_from_timestamp(answer["submission_time"])
        if answer["question_id"] == question_id:
            answers_list.append(answer_to_display_format(answer))
    write_to_csv(table, 'data/question.csv')
    return render_template("display.html", question=question_to_display, answers_list=answers_list)


@connection_handler
def add_question(question_id, new_question_data):
    table = read_from_csv('data/question.csv')
    new_question = dict()
    new_question['ID'] = question_id
    new_question['submission_time'] = generate_timestamp()
    new_question['view_number'] = 0
    new_question['vote_number'] = 0
    new_question['title'] = new_question_data['title']
    new_question['message'] = new_question_data['message']
    new_question['image'] = new_question_data['image']
    table.append(new_question)
    write_to_csv(table, 'data/question.csv')
    return redirect('/question/{}'.format(question_id))


@connection_handler
def upvote_question(id_, csv, vote):
    table = read_from_csv(csv)
    for record in table:
        print(record)
        if record['ID'] == id_:
            view_counter = int(record["view_number"]) - 1
            record["view_number"] = str(view_counter)
            # if vote == "up":
            record['vote_number'] = str(int(record["vote_number"]) + (1 if vote == "up" else -1))
            break
            # else:
            # record['vote_number'] = str(int(record["vote_number"]) - 1)
            # break
    write_to_csv(table, csv)
    return redirect("/question/{}".format(id_))
