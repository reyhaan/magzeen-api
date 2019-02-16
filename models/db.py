import os, socket, sys, time
from contextlib import contextmanager
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

#### Connection details

# We will use these settings later in the code to
# connect to the RethinkDB server.
RDB_CONFIG = {
  'host' : os.getenv('RDB_HOST', 'localhost'),
  'port' : os.getenv('RDB_PORT', 28015),
  'db'   : os.getenv('RDB_DB', 'magzeen'),
  'table': os.getenv('RDB_TABLE', 'posts')
}


# The `Connection` object returned by [`r.connect`](http://www.rethinkdb.com/api/python/connect/) 
# is a [context manager](http://docs.python.org/2/library/stdtypes.html#typecontextmanager)
# that can be used with the `with` statements.
def connection():
  return r.connect(host=RDB_CONFIG['host'], port=RDB_CONFIG['port'],
                   db=RDB_CONFIG['db'])


#### Database setup


# The app will use the table `blogposts` in the database `webpy`. 
# You can override these defaults by defining the `RDB_DB` and `RDB_TABLE`
# env variables.
# 
# We'll create the database and table here using
# [`db_create`](http://www.rethinkdb.com/api/python/db_create/)
# and
# [`table_create`](http://www.rethinkdb.com/api/python/table_create/) 
# commands.
def dbSetup():
    conn = r.connect(host=RDB_CONFIG['host'], port=RDB_CONFIG['port'])
    try:
        r.db_create(RDB_CONFIG['db']).run(conn)
        r.db(RDB_CONFIG['db']).table_create(RDB_CONFIG['table']).run(conn)
        print ('Database setup completed. Now run the app without --setup.')
    except RqlRuntimeError:
        print ('App database already exists. Run the app like this: ',
               'python blog.py')
    finally:
        conn.close()