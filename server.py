from flask import Flask, render_template, redirect, request, session, url_for
import common
import question
import answer
import users


app = Flask(__name__)


"""
Main page url Functions
"""


# main page showing only top 5 latest question comments
@app.route('/')
def index():
    criteria = request.args.get("criteria")
    order = request.args.get("order")
    limit = 5
    valid_url = common.url_validation(criteria, order)
    if not valid_url:
        return question.question_index(limit=limit)
    return question.question_index(criteria, order, limit)


# main page listing all the questions
@app.route('/list')
def index_list():
    criteria = request.args.get("criteria")
    order = request.args.get("order")
    valid_url = common.url_validation(criteria, order)
    if not valid_url:
        return question.question_index()
    return question.question_index(criteria, order)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = True
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login = users.login_to_page(username, password)
        if login:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template("login.html", login=login)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


"""
Functions related to users
"""


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    new_user = True
    if request.method == 'POST':
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        new_user = users.register_user(user_name, password)
        if new_user:
            return redirect("/")
    return render_template("registration.html", new_user=new_user)


@app.route('/user_list')
def user_list():
    return users.list_users()


"""
Functins handleing interactions with questions
"""


@app.route('/new-question')
def new_question_form():
    return question.new_question()


@app.route('/new_question', methods=['POST'])
def add_new_question():
    new_question_dict = dict()
    keys_of_form = request.form.keys()
    for key in keys_of_form:
        new_question_dict.update({key: request.form[key]})
    return question.add_question(new_question_dict)


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


@app.route("/upvote_question", methods=["POST"])
def upvote_question():
    vote = request.form.get("vote")
    id_ = request.form.get("question_id")
    username = request.form.get("username")
    return question.upvote_question(id_, vote, username)


"""
Functions responding to answer URL's
"""


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
    answer.delete_answer(answer_id)
    return redirect("/question/{}".format(question_id))


@app.route("/upvote_answer", methods=["POST"])
def upvote_answer():
    vote = request.form.get("vote")
    question_id = request.form.get("question_id")
    answer_id = request.form.get("answer_id")
    username = request.form.get("username")
    return answer.upvote(answer_id, question_id, vote, username)


"""
Functions related to comments
"""


@app.route("/question/<question_id>/new-comment")
def comment_to_question(question_id):
    return render_template("form.html", question_id=question_id, form_type="comment_to_question")


@app.route("/question/<question_id>/new-comment", methods=["POST"])
def add_comment_to_question(question_id):
    message = request.form.get("message")
    return question.comment_question(question_id, message)


@app.route("/answer/<answer_id>/new-comment")
def comment_to_answer(answer_id):
    return render_template("form.html", answer_id=answer_id, form_type="comment_to_answer")


@app.route("/answer/<answer_id>/new-comment", methods=["POST"])
def add_comment_to_answer(answer_id):
    message = request.form.get("message")
    return answer.comment_answer(answer_id, message)


@app.route("/comments/<comment_id>/delete")
def delete_comment(comment_id):
    return common.remove_comment(comment_id)


@app.route("/comments/<comment_id>/edit")
def render_comment_edit(comment_id):
    return common.edit_comment(comment_id)


@app.route('/comments/<comment_id>/edit', methods=['POST'])
def submit_edited_comment(comment_id):
    message = request.form.get("message")
    return common.submit_comment_edited(comment_id, message)


if __name__ == "__main__":
    app.secret_key = "this!is!the!secret!key"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
