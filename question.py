from flask import Flask, render_template, redirect, request, session
from common import *


# the main list.html page
def question_index():
    table = read_from_csv('data/question.csv')
    header = list()
    header.append("Question ID")
    header.append("Submission time")
    header.append("View number")
    header.append("Vote number")
    header.append("Title")
    header.append("Message")
    header.append("Image")
    return render_template('list.html', table=table, header=header)


# deleting a question by id
# redirects to /list
def delete_question(question_id):
    table = read_from_csv('data/question.csv')
    for item in table:
        if item["id"] == question_id:
            item.remowe(item)
            break
    write_to_csv(table, 'data/question.csv')
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
