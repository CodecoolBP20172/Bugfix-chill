from flask import Flask, render_template, redirect, request, session, url_for
import common
import question
import answer


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    criteria = request.args.get("criteria")
    order = request.args.get("order")
    return question.question_index(criteria, order)


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
        edit_question_dict.update({key: request.form.get(key)})
    return question.edit_question(question_id, edit_question_dict)


@app.route('/question/<question_id>/delete')
def del_question_by_id(question_id):
    return question.delete_question_with_answers(question_id)


@app.route('/question/<question_id>/new-answer')
def new_answer(question_id):
    return render_template("form.html", question_id=question_id, form_type="answer")


@app.route("/add_answer", methods=["POST"])
def add_answer():
    question_id = request.form.get("question_id")
    message = request.form.get("answer")
    image = request.form.get("image")
    return answer.post_an_answer(question_id, message, image)


@app.route('/answer/<answer_id>/delete', methods=["POST"])
def delete_answer(answer_id):
    question_id = request.form.get("question_id")
    answer.delete_answer(answer_id, question_id)
    return redirect("/question/{}".format(question_id))


@app.route("/upvote_question", methods=["POST"])
def upvote_question():
    vote = request.form.get("vote")
    id_ = request.form.get("question_id")
    return question.upvote_question(id_, vote)


@app.route("/upvote_answer", methods=["POST"])
def upvote_answer():
    vote = request.form.get("vote")
    question_id = request.form.get("question_id")
    answer_id = request.form.get("answer_id")
    return answer.upvote(answer_id, question_id, vote)


if __name__ == "__main__":
    app.secret_key = "this!is!the!secret!key"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
