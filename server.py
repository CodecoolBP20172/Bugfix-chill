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


@app.route('/add_question/<question_id>', methods=['POST'])
def add_new_question(question_id):
    new_question_dict = dict()
    keys_of_form = request.form.keys()
    for key in keys_of_form:
        print(key)
        new_question_dict.update({key: request.form[key]})
    print(new_question_dict)
    return question.add_question(question_id, new_question_dict)


@app.route('/question/<question_id>')
def display_question_by_id(question_id):
    return question.display_question(question_id)


@app.route('/question/<question_id>/edit')
def redirect_to_edit(question_id):
    return question.question_for_edit(question_id)


@app.route('/question/<question_id>/edit', methods=['POST'])
def question_edit(question_id):
    edit_question_dict = dict()
    keys_of_form = request.form.keys()
    for key in keys_of_form:
        print(key)
        edit_question_dict.update({key: request.form[key]})
    return question.edit_question(question_id, edit_question_dict)


@app.route('/question/<question_id>/delete')
def del_question_by_id(question_id):
    return question.delete_question_with_answers(question_id)


@app.route('/question/<question_id>/new-answer')
def new_answer(question_id):
    return render_template("form.html", question_id=question_id, form_type="answer")


@app.route("/add_answer", methods=["POST"])
def add_answer():
    table = common.read_from_csv('data/answer.csv')
    question_id = request.form.get("question_id")
    message = request.form.get("answer")
    return answer.post_an_answer(question_id, message)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    return answer.delete_answer(answer_id)


if __name__ == "__main__":
    app.secret_key = "this!is!the!secret!key"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
