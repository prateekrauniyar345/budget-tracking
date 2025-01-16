import psycopg2 
from flask import request, redirect, url_for, render_template
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
# realdictCursor ensures that the results are returned as a dictionary, 
# making them easy to convert them into json format. 

import datetime

# load the .env files
load_dotenv()

bcrypt = Bcrypt()

def validate_login():
    email = request.form['email']
    password = request.form['password']
    print("email is:", email)
    print("password is:", password)
    
    try:
        connection = psycopg2.connect(
            database=os.getenv('DATABASE_URL'),
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_POST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PWD'),
        )
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                print("Connection is successful.")
                query = 'SELECT * FROM users WHERE email = %s'
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                print(f"user is : {user}")
                if user:
                    if bcrypt.check_password_hash(user['password_hash'], password):
                        print("Login successful.")
                        return True, "Login successful"
                    else:
                        print("Incorrect password.")
                        return False, "Incorrect password. Please try again."
                else:
                    print("A user with such credentials does not exist.")
                    return False, "A user with such credentials does not exist."
        cursor.execute(query, new_user)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to the database:", str(error))
        return False, "Error connecting to the database"


def validate_register():
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    print("First Name:", first_name)
    print("Last Name:", last_name)
    print("Username:", username)
    print("Email:", email)
    print("Password:", password)
    print("Confirm Password:", confirm_password)

    if password != confirm_password:
        return False, "Passwords must match."

    try:
        connection = psycopg2.connect(
            database=os.getenv('DATABASE_URL'),
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_POST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PWD'),
        )
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                print("Connection is successful.")

                # Check for unique email
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                email_fetched = cursor.fetchone()

                # Check for unique username
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                username_fetched = cursor.fetchone()

                if email_fetched:
                    return False, "Email already exists."
                if username_fetched:
                    return False, "Username already taken. Choose another."

                # Insert the new user
                query = '''
                    INSERT INTO users (username, email, password_hash, first_name, last_name, role, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''
                password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                time = datetime.datetime.now()
                new_user = (
                    username, email, password_hash, first_name, last_name, 'user', time
                )
                cursor.execute(query, new_user)
                connection.commit()
                print("User registered successfully.")
                return True, "User registered successfully."
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to the database:", str(error))
        return False, "Error connecting to the database"
