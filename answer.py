from flask import Flask, render_template, redirect, request, session, url_for
from datetime import datetime
import common
import csv


def post_an_answer(question_id, message):
    table = common.read_from_csv("data/answer.csv")
    dict_into_list = {}
    dict_into_list["answer_id"] = common.id_generation(common.read_from_csv('data/answer.csv'))
    dict_into_list["time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dict_into_list["question_id"] = question_id
    dict_into_list["answer"] = message
    table.append(dict_into_list)
    common.write_to_csv(table, "data/answer.csv")
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
