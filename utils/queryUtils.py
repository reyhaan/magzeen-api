def wrap_single_quotes(value):
    return "'" + value + "'"

def generate_update_query(columns, id):
    set_string = ""
    return_string = ""
    count = len(columns)
    for key, value in columns.items():
        if not isinstance(value, int):  # wrapping single quotes around string values for SQL statement
            value = wrap_single_quotes(value)
        if count and count != 1:
            set_string += key + " = " + value + ","
            return_string += key + ","
        else:
            set_string += key + " = " + value
            return_string += key
        count = count - 1

    sql = """UPDATE users SET {} WHERE user_id={} RETURNING {};"""
    sql = sql.format(set_string, id, return_string)

    return sql
