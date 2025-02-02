#===================================================================================================
#===================================================================================================
import                                          aiosqlite
import                                          socket
import                                          time
import                                          sqlite3
import                                          time
import                                          select
import                                          asyncio
from            server_esp_fold.db_esp          import          Database
#===================================================================================================
#===================================================================================================
 

db = Database('base.db') # '../../data/base.db'

#===================================================================================================
#===================================================================================================


# Добавление-обновление данных от esp в базе данных
def process_version_1(esp_address):
    pass


# Асинхронная работа с базой данных через aiosqlite
async def add_data(temp):
    async with aiosqlite.connect('base.db') as conn:
        cursor = await conn.cursor()

        current_time = int(time.time())
        
        await cursor.execute(''' 
        INSERT INTO data (id, temp, time) VALUES (?, ?, ?) 
        ON CONFLICT(id) DO UPDATE SET temp=excluded.temp, time=excluded.time; 
        ''', (1, temp, current_time))

        await conn.commit()


async def handle_client(reader, writer, esp_address=0):

    addr = writer.get_extra_info('peername')
    print(f"Установлено соединение с {addr!r}.")

    try:
        while True:
            data = await reader.read(100)
            if not data:
                print(f"Соединение с {addr!r} закрыто клиентом.")
                break

            #================ 1 ================
            message = int(data[0])
            print('1) Длина -', message)
            #================ 2 ================
            message = int(data[1])
            print('2) Версия -', message)
            #================ 3 ================
            message = int.from_bytes(data[2:4], byteorder='little', signed=True)
            print('3) Тепмература 1 -', message)
            #================ 4 ================
            message = int.from_bytes(data[4:6], byteorder='little', signed=True)
            print('3) Тепмература 2 -', message)
            #================ 5 ================
            message = int.from_bytes(data[6:], byteorder='little', signed=False)
            print('3) Напряжение -', message)

            if int(data[1]) == 0:
                process_version_1(esp_address)

            # Эхо-ответ клиенту
            writer.write(data)
            await writer.drain()



    except ConnectionResetError:
        pass
    except Exception as e:
        print(e)
    finally:
        print(f"Закрытие соединения с {addr!r}")
        writer.close()
        try:
            await writer.wait_closed()
        except Exception as e:
            print('3')

# Функция по проверке пользователя и принятия от него ip 
async def check_client(reader, writer): # На вход подаются данные подключенного польщователя из функции server_start
    
    await handle_client(reader, writer, esp_address)


    ones = 98
    dos = 12

    writer.write(ones.to_bytes(2, byteorder='little', signed=False)) # отправка числа клиенту
    await writer.drain()

    data = await reader.read(100)
    message = int.from_bytes(data, byteorder="little", signed=False) # принятие умноженного числа от клиента


    if message == ones * dos: # Проверка числа

        data = await reader.read(100) # принятие номера esp
        esp_address = data.decode('utf-8') 

        await handle_client(reader, writer, esp_address)
    else:
        print("Проверка провалена")
    

# Запускаем сокет:
async def server_start(): 
    # Создается сервер:
    #server = await asyncio.start_server(check_client, '0.0.0.0', 8070) # При каждом подключении клиента, будет вызвана функция check_client
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8070) # При каждом подключении клиента, будет вызвана функция check_client

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets) 
    print(f'Esp Сервер запущен по адресу {addrs}')

    async with server: # Сервер запускается и начинает ожидать подключения
        await server.serve_forever()

#===================================================================================================
#===================================================================================================

async def server_esp_process(): # Запускается в main.py, принимает данные от пользователя, заносит их в base.db
    await server_start()