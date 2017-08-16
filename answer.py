# from flask import Flask, render_template, redirect, request, session, url_for
from datetime import datetime
import common
import csv


def post_an_answer():
    output_list = []
    dict_into_list = {}
    dict_into_list["answer_id"] = common.id_generation("data/answer.csv")
    dict_into_list["time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dict_into_list["question_id"] = request.form(["id_of_question"])
    dict_into_list["answer"] = common.string_to_base64(request.form(["answer"]))
    output_list.append(dict_into_list)
    return output_list


def delete_an_answer():
    id_of_answer = request.form("id_of_answer")
    with open("data/answer.csv", "w") as table:
        for record in table:
            if id_of_answer == record[2]:
                table.remove(record)
    return
