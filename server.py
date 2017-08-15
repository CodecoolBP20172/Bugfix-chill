from flask import Flask, render_template, redirect, request, session, url_for
import common
import questions
import answers

app = Flask(__name__)


@app.route('/')
@app.route('/list')


@app.route('/new-question')


@app.route('/question/<question_id>')


@app.route('/question/<question_id>/edit')


@app.route('/question/<question_id>/delete')


@app.route('/question/<question_id>/new-answer')


@app.route('/answer/<answer_id>/delete')


if __name__ == "__main__":
    app.secret_key = "this!is!the!secret!key"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
