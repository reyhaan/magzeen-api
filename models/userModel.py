import time
from database import db, config
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from utils.queryUtils import generate_update_query

class UserModel():

    def __init__(
        self,
        email=None,
        password=None,
        _type=None,
        first_name=None,
        last_name=None,
        domain_name=None,
        company_name=None
    ):
        # user_id
        # created_at
        # updated_at
        self.email = email
        self.password = password
        self.type = _type
        self.first_name = first_name
        self.last_name = last_name
        self.domain_name = domain_name
        self.company_name = company_name

    @classmethod
    def find_user_by_id(cls, id):
        sql = """SELECT user_id, email, first_name, last_name, type, company_name, domain_name FROM users WHERE user_id=%s"""
        conn = None
        user = None
        try:
            conn, cur = db.connect()
            cur.execute(sql, [id])
            user = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            return error
        finally:
            if conn is not None:
                conn.close()

        return user

    @classmethod
    def find_user_by_email(cls, email):
        sql = """SELECT * FROM users WHERE email=%s"""
        conn = None
        user = None
        try:
            conn, cur = db.connect()
            cur.execute(sql, (email,))
            user = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return user

    @classmethod
    def delete_user(cls, id):
        sql = """DELETE FROM users WHERE user_id=%s"""
        conn = None
        is_deleted = False
        try:
            conn, cur = db.connect()
            cur.execute(sql, [id])
            is_deleted = True
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return is_deleted

    @classmethod
    def update_user(cls, columns, id):
        sql = generate_update_query(columns, id)
        conn = None
        data = None
        try:
            conn, cur = db.connect()
            cur.execute(sql)
            data = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return data

    @classmethod
    def verify_user(cls, email, password):
        sql = """SELECT * FROM users WHERE email=%s AND password=%s"""
        conn = None
        user = None
        count = 0
        password = check_password_hash(password)
        try:
            conn, cur = db.connect()
            cur.execute(sql, (email, password))
            user = cur.fetchone()
            if user is not None:
                count = len(user)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return count

    @classmethod
    def check_if_user_exists_by_email(cls, email):
        sql = """SELECT * FROM users WHERE email=%s"""
        conn = None
        count = 0
        user = None
        try:
            conn, cur = db.connect()
            cur.execute(sql, (email,))
            user = cur.fetchone()
            if user is not None:
                count = len(user)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return count

    @classmethod
    def check_if_user_exists_by_id(cls, id):
        sql = """SELECT * FROM users WHERE user_id=%s"""
        conn = None
        count = 0
        user = None
        try:
            conn, cur = db.connect()
            cur.execute(sql, [id])
            user = cur.fetchone()
            if user is not None:
                count = len(user)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return count

    @classmethod
    def add_user(cls, email, password):
        password = generate_password_hash(password)
        sql = """INSERT INTO users(email, password)
                VALUES(%s, %s) RETURNING (user_id, email);"""
        conn = None
        user = None
        try:
            conn, cur = db.connect()
            cur.execute(sql, (email, password,))
            user = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return user
