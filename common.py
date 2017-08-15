import csv
import base64


def read_from_csv(csvfile):  #Debi
    with open(csvfile) as csvfile:
        list_of_questions = csv.DictReader(csvfile)
        questions = []
        for row in list_of_questions:
            questions.append(row)
        return questions


def write_to_csv():  #Gábor
    pass


def string_to_base64(origin):
    origin_in_bytes = origin.encode('utf-8')
    b64_encoded_bytes = base64.b64encode(origin_in_bytes)
    return b64_encoded_bytes.decode('utf-8')


def base64_to_string(encoded_string):
    decoded_string = base64.b64decode(encoded_string)
    return decoded_string.decode('utf-8')


def print_info(variable):
    print("Original string: {var} ({type})".format(**{
        "var": variable,
        "type": type(variable)
    }))
