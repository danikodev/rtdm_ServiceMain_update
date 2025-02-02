#===================================================================================================
#===================================================================================================


import sqlite3

#===================================================================================================
#===================================================================================================

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False) # check_same_thread=False - убрать ошибку подключения из разнах потоков
        self.cursor = self.connection.cursor()

#===================================================================================================
#===================================================================================================

    def add_users(self, users_address):
        with self.connection:
            insert_query = """
            INSERT INTO users (users_address)
            VALUES (?);
            """
            return self.cursor.execute(insert_query, (users_address,))
        
    def add_esp(self, esp_address):
        with self.connection:
            insert_query = '''
            INSERT INTO esp (esp_address)
            VALUES (?); 
            '''
            return self.cursor.execute(insert_query, (esp_address,))
        
    def get_esp_address_id(self, esp_address):
        with self.connection:
            select_query = """
            SELECT id
            FROM esp
            WHERE esp_address = ?;
            """
            self.cursor.execute(select_query, (esp_address,))

            return (self.cursor.fetchone())[0]
    
    def get_users_address_id(self, users_address_telegram):
        with self.connection:
            select_query = """
            SELECT id
            FROM users
            WHERE users_address_telegram = ?;
            """
            self.cursor.execute(select_query, (users_address_telegram,))

            return (self.cursor.fetchone())[0]


    def add_connection(self, users_address, esp_address):
        with self.connection:

            users_address_id = self.get_users_address_id(users_address)
            esp_address_id = self.get_esp_address_id(esp_address)

            insert_query = """
            INSERT INTO connections (users_address_id, esp_address_id)
            VALUES (?, ?);
            """
            
            return self.cursor.execute(insert_query, (users_address_id, esp_address_id))
    def is_users_signup(self, users_address_telegram): # << исправить =============================================================
        with self.connection:
            self.cursor.execute("SELECT 1 FROM users WHERE users_address_telegram = ?", (users_address_telegram,)) 
            users_exists = self.cursor.fetchone()

            return users_exists
        
    def is_esp_signup(self, esp_address):
        with self.connection:
            self.cursor.execute("SELECT 1 FROM esp WHERE esp_address = ?", (esp_address,))
            esp_exists = self.cursor.fetchone()

            return esp_exists is not None  # Вернёт True, если устройство найдено, и False, если нет

    def is_esp_connect(self, esp_address, users_address):
        with self.connection:
            users_address_id = self.get_users_address_id(users_address)
            esp_address_id = self.get_esp_address_id(esp_address)

            self.cursor.execute(
            "SELECT 1 FROM connections WHERE users_address_id = ? AND esp_address_id = ?",
            (users_address_id, esp_address_id)
            )

            connection_exists = self.cursor.fetchone()

            return connection_exists is not None

    def registretion(self, users_address_telegram, esp_address):

        if not self.is_users_signup(users_address_telegram):
            self.add_users(users_address_telegram)

        if not self.is_esp_signup(esp_address):
            self.add_esp(esp_address)

        self.add_connection(users_address_telegram, esp_address)

    


#===================================================================================================
#===================================================================================================


