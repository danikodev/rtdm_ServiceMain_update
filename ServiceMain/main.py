#===================================================================================================
#===================================================================================================
import                                                      asyncio

from        server_esp_fold.server_esp                      import          server_esp_process
from        server_telegram_fold.server_telegram_bot        import          server_telegram_bot_process
#===================================================================================================
#===================================================================================================

async def main():

    # Запускаем серверы как асинхронные задачи
    task_server_esp = asyncio.create_task(server_esp_process())
    task_server_telegram_bot = asyncio.create_task(server_telegram_bot_process())
    # task_server_yandex = asyncio.create_task(server_yandex_process())

    # Ожидаем завершения всех задач
    await asyncio.gather(task_server_esp, task_server_telegram_bot) # , task_server_yandex





if __name__ == "__main__":
    asyncio.run(main())