import csv
import base64


def read_from_csv(input_file):
    with open(input_file) as input_file:
        list_of_questions = csv.DictReader(input_file)
        questions = []
        for row in list_of_questions:
            questions.append(row)
        for row in questions:
            for key, value in row.items():
                if key in ("title", "message", "image"):
                    row[key] = base64_to_string(value)
                else:
                    continue
        return questions


def write_to_csv(data, output_file):
    headers = ["ID", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    for row in data:
        for key, value in row.items():
            if key in ("title", "message", "image"):
                row[key] = string_to_base64(value)
    with open(output_file, "w") as output_file:
        dict_writer = csv.DictWriter(output_file, headers)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    return


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


def id_generation(table):
    with open(table, "r") as table:
        id_list = []
        generated_id = 0
        for data in table:
            id_list.append(int(data[0]))
        generated_id = max(id_list) + 1
    return(generated_id)
