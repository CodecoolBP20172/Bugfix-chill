import psycopg2
from config import Config


def main():
    connection = psycopg2.connect(Config.DB_CONNECTION_STR)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(open("sample_data/askmatepart2-sample-data.sql", "r").read())

    cursor.execute("UPDATE question SET username = 'Xattus'")
    cursor.execute("UPDATE answer SET username = 'Xattus'")
    cursor.execute("UPDATE comment SET username = 'Xattus'")


if __name__ == "__main__":
    main()
