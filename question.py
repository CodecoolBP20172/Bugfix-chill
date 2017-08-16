from flask import Flask, render_template, redirect, request, session
from common import *
import datetime


# the main list.html page
def question_index():
    table = read_from_csv('data/question.csv')
    for row in table:
        for key, value in row.items():
            if key == "submission_time":
                row[key] = date_from_timestamp(value)
    header = ["ID", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    return render_template('list.html', table=table, header=header)


def delete_question(question_id):
    table = read_from_csv('data/question.csv')
    for question in table:
        if question["ID"] == question_id:
            table.remove(question)
            break
    write_to_csv(table, 'data/question.csv')


def delete_answers_for_question_id(question_id):
    answer_table = read_from_csv('data/answer.csv')
    for answer in answer_table:
        if answer['question_id'] == question_id:
            answer_table.remove(answer)
    write_to_csv(answer_table, 'data/answer.csv')


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
def edit_question(question_id, edited_question):
    table = read_from_csv('data/question.csv')
    for index, question in enumerate(table):
        if question["ID"] == question_id:
            table[index] = edited_question
    write_to_csv(table, 'data/question.csv')
    return redirect('/list')


# redirects to the question submitting page with a new id for the question
def new_question():
    table = read_from_csv('data/question.csv')
    new_id = id_generation(table)
    return render_template("/form.html", id=new_id, form_type="add_question")


def display_question(question_id):
    table = read_from_csv('data/question.csv')
    answers_list = list()
    question_to_display = None
    for question in table:
        if question["ID"] == question_id:
            question_to_display = question
            break
    answer_table = read_from_csv('data/answer.csv')
    for answer in answer_table:
        if answer["question_id"] == question_id:
            answers_list.append(answer)
    print(answers_list)
    return render_template("display.html", question=question_to_display, answers_list=answers_list)


def add_question(question_id, new_question_data):
    table = read_from_csv('data/question.csv')
    new_question = dict()
    new_question['ID'] = question_id
    new_question['submission_time'] = generate_timestamp()
    new_question['view_number'] = 0
    new_question['vote_number'] = 0
    new_question['title'] = new_question_data['question-title']
    new_question['message'] = new_question_data['message']
    new_question['image'] = ''
    table.append(new_question)
    print(table)
    write_to_csv(table, 'data/question.csv')
    return redirect('/question/{}'.format(question_id))
