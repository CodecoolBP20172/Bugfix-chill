from config import Config
import psycopg2
import psycopg2.extras


def open_database():
    try:
        connection_string = Config.DB_CONNECTION_STR
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print(exception)
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a dict cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value
    return wrapper


""" I think id_generation is not nessescary anymore as the tables generate the ids with a sequence """


def id_generation(table):
    try:
        id_list = []
        for data in table:
            id_list.append(int(data['ID']))
        generated_id = max(id_list) + 1
    except ValueError:
        generated_id = 0
    return(generated_id)


@connection_handler
def ordering(cursor, criteria, order, limit):
    if criteria and order:
        order_dict = {'criteria': criteria, 'order': order, 'limit': limit}
        if limit:
            cursor.execute("SELECT * FROM question ORDER BY {criteria} {order} LIMIT {limit}; \
                        ".format(criteria=order_dict['criteria'], order=order_dict['order'], limit=order_dict['limit']))
        else:
            cursor.execute("SELECT * FROM question ORDER BY {criteria} {order}; \
                        ".format(criteria=order_dict['criteria'], order=order_dict['order']))
    else:
        cursor.execute("SELECT * FROM question ORDER BY id ASC;")
    table = cursor.fetchall()
    return table
