import time
import rethinkdb as r
import db


def getUser(self):
    return 'a user'


def deleteUser(self):
    return 'user deleted'


def addUser(self, username, password):
    new_user = {
        'username': username,
        'password': password,
        'created_at': time.time(),
        'updated_at': time.time()
    }
    with db.connection() as conn:
        result = r.table(
            db.RDB_CONFIG['table']['users']
        ).insert(new_user).run(conn)
        if result['inserted'] == 1:
            new_user['id'] = result['generated_keys'][0]
            return new_user
        else:
            return None
