import mysql.connector
from mysql.connector import Error

#insert images into the SQL DB
def insert_images(pic, num):
    note = "Pic" + str(num)

    query = "INSERT INTO images (image, notes) VALUES(%s, %s)"
    args = (pic, note)

    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='ecen404',
                                            user='root',
                                            password='ecen404',
                                            charset='utf8mb4')


        if connection.is_connected():

            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            cursor.execute(query,args)

    except Error as e:
        print("Error while connecting to MySQL", str(e)[0:100])
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def getImagesFromDB():

    query = "SELECT * FROM images"
    

    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='ecen404',
                                            user='root',
                                            password='ecen404',
                                            charset='utf8mb4')


        if connection.is_connected():

            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            cursor.execute(query)
            record = cursor.fetchall()
            for row in record:
                fullFileName = "C:\\Users\\Braden\\Desktop\\ECEN 404\\FromDatabase\\" + str(row[2]) + ".jpg"
                write_file(row[1], fullFileName)
            

    except Error as e:
        print("Error while connecting to MySQL", str(e)[0:100])
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def clearDatabase():
    query = "DELETE FROM images; ALTER TABLE images auto_increment=0;"

    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='ecen404',
                                            user='root',
                                            password='ecen404',
                                            charset='utf8mb4')


        if connection.is_connected():
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            cursor.execute(query)

    except Error as e:
        print("Error while connecting to MySQL", str(e)[0:100])

    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")