
import mysql.connector

def get_connection():

    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="python_bank"
        )

        if con.is_connected():
            print("Database connected successfully!")

        return con

    except mysql.connector.Error as e:
        print("Connection error:", e)
        return None
