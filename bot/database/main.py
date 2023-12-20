from .methods.create import initialize_database
from .methods.delete import delete_word_from_history, delete_user
from .methods.update import add_new_user, check_and_add_word, remember_word
from .methods.get import retrieve_user_history

import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def initialize_database(self):
        initialize_database()

    def delete_word_from_history(self, word_id):
        delete_word_from_history()

    def delete_user(self, user_id):
        delete_user()

    def add_new_user(self, user_data):
        add_new_user()

    def check_and_add_word(self, user_id, word):
        check_and_add_word()

    def remember_word(self, user_id, word):
        remember_word()

    def retrieve_user_history(self, user_id):
        retrieve_user_history()

