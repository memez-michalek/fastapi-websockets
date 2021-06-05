import psycopg2
from models import modelHandler
import bcrypt

def QueryUserByEmail(input_user: modelHandler.UserIn, cursor):
    cursor.execute("""SELECT * FROM CREDS WHERE email='%s'""" % input_user.email)
    data = cursor.fetchall()
    print(data)
    if data == []:
        return False
    else:
        return True

def InitDb():
    try:
        conn = psycopg2.connect(
            user="postgres",
            host="localhost",
            password="password",
            database="USERS",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f'error occurred {e}')
        return None

def LoginUser(input_user: modelHandler.UserIn):
    connection = InitDb()
    cursor = connection.cursor()
    if cursor != None:
        exists = QueryUserByEmail(input_user, cursor)
        if exists == True:
            cursor.execute("""SELECT * FROM CREDS WHERE email='%s'""" % input_user.email)
            users_data  = cursor.fetchone()
            print(bytes(users_data[3]))
            result = bcrypt.checkpw(input_user.password.encode("utf-8"), bytes(users_data[3]))
            
            if result == True:
                print("everything went smoothly")
                return (True, users_data[0], "",200)
            else:
              print("incorrect password")
              return (False,"incorrect password",403)  
        else:
            print("error with particular email does not exist")
            return (False, "error with particular email does not exist",403)
    else:
        print("internal cursor creation error ")
        return (False, "internal cursor creation error ",500)

def RegisterUser(input_user: modelHandler.UserIn):
    conn = InitDb()
    cursor = conn.cursor()
    if input_user.username != "" and input_user.password != "":
        if cursor != None:
            user_exist = QueryUserByEmail(input_user,cursor)
            if user_exist != True:
                hashed_pw = bcrypt.hashpw(bytes(input_user.password, 'utf-8'), bcrypt.gensalt(14))
                db_template = modelHandler.DBIn(**input_user.dict(), hashedpassword=hashed_pw)
                try:
                    cursor.execute("INSERT INTO CREDS(email,username,password) VALUES(%s,%s,%s)", (db_template.email, db_template.username, db_template.hashedpassword))
                    conn.commit()
                    cursor.execute("""SELECT * FROM CREDS WHERE email='%s'""" % input_user.email)
                    id = cursor.fetchone()[0]
                    return (True, id, "", 200)
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                    return (False, error, 500)
            else:
                print("user already exists")
                return (False, "user already exists", 400)

        else:
            print("could not instantiate database connection")
            return (False, "internal error", 500)

    else:
        print("form data is missing")
        return (False, "form data is missing", 403)

