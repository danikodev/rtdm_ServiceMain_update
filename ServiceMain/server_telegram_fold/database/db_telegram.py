#===================================================================================================
#===================================================================================================

import math
import sqlite3
import itertools

#===================================================================================================
#===================================================================================================

class Paginator:
    def __init__(self, array: list | tuple, page: int=1, per_page: int=1):
        self.array = array
        self.per_page = per_page
        self.page = page
        self.len = len(self.array)
        # math.ceil - округление в большую сторону до целого числа
        self.pages = math.ceil(self.len / self.per_page)

    def __get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self):
        page_items = self.__get_slice()
        return page_items

    def has_next(self):
        if self.page < self.pages:
            return self.page + 1
        return False

    def has_previous(self):
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self):
        if self.page < self.pages:
            self.page += 1
            return self.get_page()
        raise IndexError(f'Next page does not exist. Use has_next() to check before.')

    def get_previous(self):
        if self.page > 1:
            self.page -= 1
            return self.__get_slice()
        raise IndexError(f'Previous page does not exist. Use has_previous() to check before.')
    
#===================================================================================================
#===================================================================================================

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file,)
        self.cursor = self.connection.cursor()


    def get_user_address_id(self, user_address_telegram):
        with self.connection:

            select_query = """
                SELECT id
                FROM users
                WHERE users_address_telegram = ?;
                """
            self.cursor.execute(select_query, (user_address_telegram, ))
            
            result = self.cursor.fetchone()

            if result:
                return result[0]
            else:
                return None
        
    def get_list_esp_address_id(self, user_address_telegram):
        with self.connection:

            user_address_id = self.get_user_address_id(user_address_telegram)

            select_query = """
                SELECT esp_address_id
                FROM connections
                WHERE users_address_id = ?;
                """
            self.cursor.execute(select_query, (user_address_id, ))
            
            result = self.cursor.fetchall()

            result = list(itertools.chain(*result)) # [(3,), (4,), (5,), (6,), (7,), (1,)]  --->  [3, 4, 5, 6, 7, 1]

            if result:
                return result
            else:
                return None
            
    # Принимает user_address_telegram, а отдает данные о всех привязанных к нему термометрах в виде двухмерного списка
    # [[45.0, 33.0, 99.9, 33.0, None], [9.0, 9.0, 9.0, 9.0, None], [0, 0, 0, 0, False]]
    def get_esp_parameters(self, user_address_telegram):
        with self.connection:

            list_esp_address_id = self.get_list_esp_address_id(user_address_telegram)

            result = []
            sc = 0
            for esp_address_id in list_esp_address_id:

                select_query = '''
                SELECT temp_1, temp_2, voltage_1, voltage_2, time
                FROM parameters
                WHERE esp_address_id = ?; 
                '''
                self.cursor.execute(select_query, (esp_address_id, ))
                data = self.cursor.fetchone()

                if data:
                    data = list(data)
                else:
                    data = [0, 0, 0, 0, None]

                # print(data)
                result.append(data)

            return result

    
    def is_user_address_telegram_in_base(self, user_address_telegram):
        with self.connection:
            query = '''
            SELECT * FROM users 
            WHERE users_address_telegram = ?; 
            '''
            self.cursor.execute(query, (user_address_telegram,))
            result = self.cursor.fetchone()
            if result:
                return True
            else:
                return False

    def add_user_address_telegram_in_base(self, user_address_telegram):
        with self.connection:
            insert_query = '''
            INSERT INTO users (users_address_telegram)
            VALUES (?); 
            '''
            return self.cursor.execute(insert_query, (user_address_telegram,))
        

    def update_user_telegram_location_data(self, user_address_telegram, message_id, level, page):
        with self.connection:
            update_query = '''
            UPDATE users
            SET message_id = ?,
                level = ?,
                page = ?
            WHERE users_address_telegram = ?;
            '''
            return self.cursor.execute(update_query, (message_id, level, page, user_address_telegram))

    def get_user_telegram_location_data(self, user_address_telegram):
        with self.connection:
            select_query = """
            SELECT message_id, level, page
            FROM users
            WHERE users_address_telegram = ?;
            """
            self.cursor.execute(select_query, (user_address_telegram,))

            result = self.cursor.fetchone()
            if result:
                return list(result)
            else:
                return None


    def is_user_telegram_location_current(self, user_address_telegram, message_id, level, page):
        with self.connection:
            user_telegram_location_data = self.get_user_telegram_location_data(user_address_telegram)
            
            if [message_id, level, page] == user_telegram_location_data:
                return True
            else:
                return False


#===================================================================================================
#===================================================================================================
