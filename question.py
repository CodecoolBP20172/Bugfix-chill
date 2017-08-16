from flask import Flask, render_template, redirect, request, session
from common import *


# the main list.html page
def question_index():
    table = read_from_csv('data/question.csv')
    header = ["ID", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    return render_template('list.html', table=table, header=header)


# deleting a question by id
# redirects to /list
def delete_question(question_id):
    table = read_from_csv('data/question.csv')
    for question in table:
        if question["ID"] == question_id:
            table.remove(question)
            break
    write_to_csv(table, 'data/question.csv')
    return redirect('/list')


# editing a question by id
# replaces the question with the one gets from the form
# redirects to /list
def edit_question(question_id, edited_question):
    table = read_from_csv('/data/question.csv')
    for index, question in enumerate(table):
        if question["ID"] == question_id:
            table[index] = edited_question
    write_to_csv(table, 'data/question.csv')
    return redirect('/list')


def new_question(form_content):
    table = read_from_csv('data/question.csv')
    print(from_content)
    table.append(form_content)
    write_to_csv(table, 'data/question.csv')
    return redirect("/")


def display_question(question_id):
    table = read_from_csv('data/question.csv')
    question_to_display = None
    for question in table:
        if question["ID"] == question_id:
            question_to_display = question
            break
    return render_template("display.html", question=question_to_display)
