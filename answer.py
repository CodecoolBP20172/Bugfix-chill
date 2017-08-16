from flask import Flask, render_template, redirect, request, session, url_for
from datetime import datetime
import common
import csv


def post_an_answer(question_id):
    output_list = []
    dict_into_list = {}
    dict_into_list["answer_id"] = common.id_generation("data/answer.csv")
    dict_into_list["time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dict_into_list["question_id"] = request.form(["id_of_question"])
    dict_into_list["answer"] = common.string_to_base64(request.form(["answer"]))
    output_list.append(dict_into_list)
    return render_template("display.html")


def delete_answer(answer_id):
    table = common.read_from_csv('data/answer.csv')
    for item in table:
        if item["ID"] == answer_id:
            table.remove(item)
            break
    common.write_to_csv(table, 'data/answer.csv')
    return render_template("display.html")
