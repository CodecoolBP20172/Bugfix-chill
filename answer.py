from flask import Flask, render_template, redirect, request, session, url_for
from datetime import datetime
from common import *


@connection_handler
def post_an_answer(cursor, question_id, message, image):
    cursor.execute("INSERT INTO answer (submission_time, vote_number, question_id, message, image) VALUES "
                   "(%s, %s, %s, %s, %s);", (datetime.now(), 0, question_id, message, image))
    return redirect("/question/{}".format(question_id))


def delete_answer(answer_id):
    table = common.read_from_csv('data/answer.csv')
    for item in table:
        if item["ID"] == answer_id:
            question_id = item['question_id']
            table.remove(item)
            break
    common.write_to_csv(table, 'data/answer.csv')
    return redirect('/question/{}'.format(question_id))


def upvote(id_, csv, question_id, vote):
    table = common.read_from_csv(csv)
    for record in table:
        print(record)
        if record['ID'] == id_:
            if vote == "up":
                record['vote_number'] = str(int(record["vote_number"]) + 1)
                break
            else:
                record['vote_number'] = str(int(record["vote_number"]) - 1)
                break
    common.write_to_csv(table, csv)
    return redirect("/question/{}".format(question_id))
