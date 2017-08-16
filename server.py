from flask import Flask, render_template, redirect, request, session, url_for
import common
import question
import answer

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    return question.question_index()


@app.route('/new-question')
def new_question_form():
    return question.new_question()


@app.route('/add_question/<question_id>')
def add_new_question(question_id):
    return question.add_question(question_id, request.form)


@app.route('/question/<question_id>')
def display_question_by_id(question_id):
    return question.display_question(question_id)


@app.route('/question/<question_id>/edit')
def question_edit(question_id):
    form_keys = request.form.keys()
    edited_question = dict()
    for key in form_keys:
        edited_question.update({key: request.form[key]})
    return question.edit_question(question_id, edited_question)


@app.route('/question/<question_id>/delete')
def del_question_by_id(question_id):
    return question.delete_question_with_answers(question_id)


@app.route('/question/<question_id>/new-answer')
def new_answer(question_id):
    return answer.post_an_answer(question_id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    return answer.delete_answer(answer_id)


if __name__ == "__main__":
    app.secret_key = "this!is!the!secret!key"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
