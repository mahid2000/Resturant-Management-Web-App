import sqlite3
from flask import current_app


class DBManager:
    _created = False

    def __init__(self, app):
        self.db = self._create_db(app)
        self.cursor = self.db.cursor()

    def get_db(self):
        """Gets the database connection."""
        return self.db

    def get_connection(self):
        """Gets a cursor to communicate to the database with."""
        return self.cursor

    def close(self):
        """Close the cursor and the connection."""
        self._close_cursor()
        self._close_db()

    def _close_cursor(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None

    def _close_db(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    @staticmethod
    def _create_db(app):
        """Connects to the database and returns the connection. Creates the database if it hasn't been created since
        starting the program."""
        db = sqlite3.connect("database.db")

        # If the database hasn't been created yet, create it
        # This is because connecting to the database happens in each webpage method,
        # and we don't want to re-create the database every time we reload or change page
        if not DBManager._created:
            with app.app_context():
                with current_app.open_resource('static/schema.sql') as file:
                    db.executescript(file.read().decode('utf8'))
                    DBManager._created = True

        return db
