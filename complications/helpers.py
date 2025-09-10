import sqlite3


class SQLiteDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    # Open database connection
    def open(self):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row # Create rows for import to Jinja
        self.cursor = self.connection.cursor()

    # Close database connection
    def close(self):
        if self.connection:
            self.connection.close()

    # Execute queries
    def execute(self, query, params=None, fetch=False):
        if not self.connection:
            raise Exception("No connection established")

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            if fetch:
                result = [dict(row) for row in self.cursor.fetchall()]
                return result # If results needed from query than return fetchall
            else:
                self.connection.commit()    # Else commit changes

        except sqlite3.Error:
            return None

def query(database, query, params=None, fetch=False):
    database.open()
    if fetch:
        result = database.execute(query, params, fetch)
        database.close()
        return result
    else:
        database.execute(query,params,fetch)
        database.close()
        return

