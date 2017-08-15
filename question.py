from flask import Flask, render_template, redirect, request, session
from common import *


# the main list.html page
def question_index():
    table = read_from_csv('/data/question.csv')
    return render_template('list.html', table=table)


# deleting a question by id
# redirects to /list
def delete_question(question_id):
    table = read_from_csv('/data/question.csv')
    for item in table:
        if item["id"] == question_id:
            item.remowe(item)
            break
    write_to_csv(table, '/data/question.csv')
    return redirect('/list')


# editing a question by id
# replaces the question with the one gets from the form
# redirects to /list
def edit_question(question_id, edited_question):
    table = read_from_csv('/data/question.csv')
    for index, item in enumerate(table):
        if item["id"] == question_id:
            table[index] = edited_question
    return redirect('/list')
