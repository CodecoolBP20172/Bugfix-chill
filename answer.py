from flask import Flask, render_template, redirect, request, session, url_for
from datetime import datetime
import common
import csv


def post_an_answer():
    output_list = []
    dict_into_list = {}
    dict_into_list["answer_id"] = "todo, waiting for the func. to be made"
    dict_into_list["time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dict_into_list["question_id"] = "here's a random ID"
    dict_into_list["answer"] = common.string_to_base64("bla bla bla helpful shit")
    output_list.append(dict_into_list)
    return output_list
