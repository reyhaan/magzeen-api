def wrap_single_quotes(value):
    return "'" + value + "'"

def generate_update_query(columns, id):
    set_string = ""
    values_string = ""
    count = len(columns)
    for key, value in columns.items():
        if not isinstance(value, int):
            value = wrap_single_quotes(value)
        if count and count != 1:
            set_string += key + " = " + value + ","
        else:
            set_string += key + " = " + value
        count = count - 1

    sql = """UPDATE users SET {} WHERE user_id={};"""
    sql = sql.format(set_string, id)

    return sql
