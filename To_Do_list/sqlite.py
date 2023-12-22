import sqlite3

connection  = sqlite3.connect ("db.sqlite")

cursor = connection.cursor()

create_table_sql = '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_text TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    )
'''

#element_id = 1 # Replace with the ID of the element you want to delete

#cursor.execute("DELETE FROM your_table WHERE id = ?", (element_id,))

cursor.execute(create_table_sql)

connection.commit()

connection.close()