from .methods.create import initialize_database
from .methods.delete import delete_word_from_history, delete_user
from .methods.update import add_new_user, check_and_add_word, remember_word
from .methods.get import retrieve_user_history

import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name  

    def initialize_database(self):
        return initialize_database(db_name=self.db_name)

    def delete_word_from_history(self, user_id, word_id):
        return delete_word_from_history(user_id=user_id, word_id=word_id, db_name=self.db_name)

    def delete_user(self, user_id):
        return delete_user(user_id=user_id, db_name=self.db_name)

    def add_new_user(self, user_id):
        return add_new_user(user_id=user_id, db_name=self.db_name)

    def check_and_add_word(self, user_id, word, to_language, from_language): # TODO: add to_language and from_language
        return check_and_add_word(user_id=user_id, word=word, db_name=self.db_name, to_language=to_language, from_language=from_language)

    def remember_word(self, user_id, word, to_language, from_language):
        return remember_word(user_id=user_id, word=word, db_name=self.db_name, to_language=to_language, from_language=from_language)

    def retrieve_user_history(self, user_id):
        return retrieve_user_history(user_id=user_id, db_name=self.db_name)
        
