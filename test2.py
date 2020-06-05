import mysql.connector
from mysql.connector import Error


def file_binary(filename):
    with open(filename, 'rb') as file:
        binary = file.read()
    return binary


def inBlob(id, file):
    print("entering data \n")
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='lucifer123#321',
            database='files'
        )

        cursor = conn.cursor()

        sql_formula = """ INSERT INTO file_bin
                    (id, file_name) VALUES (%s,%s)"""

        file = file_binary(file)

        blob_tuple = (id, file)
        result = cursor.execute(sql_formula, blob_tuple)
        conn.commit()
        print("files has been inserted")

        cursor.close()
        conn.close()
    except mysql.connector.Error as error:
        print("failed {}".format(error))


inBlob(1, "input_valid.txt")
