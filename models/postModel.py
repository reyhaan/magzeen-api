import os, socket, sys, time
from contextlib import contextmanager
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError
import db

#### Listing existing posts

# To retrieve all existing tasks, we are using the
# [`r.table`](http://www.rethinkdb.com/api/python/table/)
# command to query the database in response to a GET request from the
# browser. We also [`order_by`](http://www.rethinkdb.com/api/python/order_by/)
# the `posted_at` attribute in a descending manner.
#    
# Running the query returns an iterator that automatically streams
# data from the server in efficient batches.
def get_posts():
  with db.connection() as conn:
    return (r.table(db.RDB_CONFIG['table'])
             .order_by(r.desc('posted_at')).run(conn))

#### Creating a new post

# We create a new blog entry using
# [`insert`](http://www.rethinkdb.com/api/python/insert/).
#
# The `insert` operation returns a single object specifying the number
# of successfully created objects and their corresponding IDs:
#
# ```
# {
#   "inserted": 1,
#   "errors": 0,
#   "generated_keys": [
#     "b3426201-9992-4a21-ab84-974603657671"
#   ]
# }
# ```
def new_post(title, text):
  new_post = {'title': title, 
    'content': text, 
    'posted_at': time.time(),
    'last_modified': time.time()
  }
  with db.connection() as conn:
    result = r.table(db.RDB_CONFIG['table']).insert(new_post).run(conn)
    if result['inserted'] == 1:
      new_post['id'] = result['generated_keys'][0]
      return new_post
    else:
      return None

#### Retrieving a single post

# Every new post gets assigned a unique ID. The browser can retrieve
# a specific task by GETing `/view/<post_id>`. To query the database
# for a single document by its ID, we use the
# [`get`](http://www.rethinkdb.com/api/python/get/)
# command.
def get_post(id):
  with db.connection() as conn:
    return r.table(db.RDB_CONFIG['table']).get(id).run(conn)

#### Updating a post

# To update the post we'll use the 
# [`update`](http://www.rethinkdb.com/api/python/update/)
# command, which will merge the JSON object stored in the database with the
# new one.
#
# The `update` operation returns an object specifying how many rows
# have been updated.
def update_post(id, title, text):
  with db.connection() as conn:
    result = (r.table(db.RDB_CONFIG['table']).get(id)
               .update({'title': title, 'content': text,
                        'last_modified': time.time()})
               .run(conn))
    return result.get('modified', 0) == 1

#### Deleting a post

# To delete a post we'll call a
# [`delete`](http://www.rethinkdb.com/api/python/delete/)
# command.
#
# The `delete` operation returns an object specifying how many
# rows have been deleted.
def del_post(id):
  with db.connection() as conn:
    result = r.table(db.RDB_CONFIG['table']).get(id).delete().run(conn)
    return result.get('deleted', 0) == 1