import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ParseMode
from aiogram.dispatcher.filters import Text
API_TOKEN = '5725900458:AAG7tV_nDgroqqTK4ZGHMY05jMkA9wAQNcg'
GROUP_ID_FILE = 'group_ids.txt'
admins = [1893838178,]
user_data = {}
user_data[admins[0]] = {}
# with open(filename) as file:
#     while (line := file.readline().rstrip()):
#         print(line)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

group_ids = []

def write_group_id_to_file(group_id):
    with open(GROUP_ID_FILE, 'a') as f:
        f.write(str(group_id) + '\n')

@dp.message_handler(commands='get_groups')
async def cmd_get_groups(message: Message):
    result = 'The bot is a member of the following group chats:\n'
    for group_id in group_ids:
        result += f' - {group_id}\n'
    await bot.send_message(chat_id=message.chat.id, text=result)

@dp.message_handler(commands='send_to_groups')
async def cmd_send_to_groups(message: Message):
    if message.from_user.id in admins:
        await message.answer("PLEASE SEND ME YOUR MESSAGE")
    # for group_id in group_ids:
    #     await bot.send_message(chat_id=group_id, text=message.text[15:])


@dp.message_handler(commands='savethisgroup')
async def handle_group_join(message: Message):
    group_id = message.chat.id
    if group_id not in group_ids:
        write_group_id_to_file(group_id)
        group_ids.append(group_id)

@dp.message_handler(Text(equals=["YES", "NO"]))
async def handle_choices(message: types.Message):
    if message.text == "YES" and message.from_user.id in admins:
        try:
            message_id = user_data[message.from_user.id]["message_id"]
            for group_id in group_ids:
                await bot.forward_message(chat_id=group_id, message_id=message_id, from_chat_id=message.chat.id)
        except Exception as e:
            print(str(e))
            await message.answer("There was an error with your request.\nPlease check the information you entered and try again.")
    else:
        await message.answer("I UNDERSTAND.\nIF YOU WANT TO SEND MESSAGE YOUR GROUPS.\nI ALWAYS READY")


@dp.message_handler(content_types=['photo', 'video', 'text'])
async def handle_sender_message(message: Message):
    ynkb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    ybt = types.KeyboardButton("YES")
    nbt = types.KeyboardButton("NO")
    ynkb.add(ybt, nbt)
    if  not message.chat.type in ["group", "channel"]:
        if message.from_user.id in admins:
            user_data[message.from_user.id]["message_id"] = message.message_id
            await message.reply("DO YOU WANT SEND THIS MESSAGE TO ALL GROUP", reply_markup=ynkb)
        else:
            await message.reply("YOU DON'T HAVE THIS PERMISSION")

        

if __name__ == '__main__':
    if not os.path.exists(GROUP_ID_FILE):
        open(GROUP_ID_FILE, 'w').close()
    else:
        with open(GROUP_ID_FILE, 'r') as f:
            for line in f:
                group_ids.append(int(line.strip()))
    executor.start_polling(dp, skip_updates=True)
