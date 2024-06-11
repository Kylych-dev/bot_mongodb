from aiogram.filters import CommandStart, Command
from aiogram import Bot, types, Dispatcher
import asyncio, logging, json

from core.settings import BOT_TOKEN
from core.aggregation import aggregate_data

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



@dp.message()
async def handle_message(msg: types.Message):
    try:
        request_data = json.loads(msg.text)
        dt_from = request_data['dt_from']
        dt_upto = request_data['dt_upto']
        group_type = request_data['group_type']

        response_data = aggregate_data(dt_from, dt_upto, group_type)

        sorted_labels = sorted(response_data['labels'])

        sorted_labels_data = {
            'dataset': response_data['dataset'],
            'labels': sorted_labels
        }

        await msg.answer(text=json.dumps(sorted_labels_data))
    except (json.JSONDecodeError, KeyError) as ex:
        await msg.answer(text='Допустимо отправлять только следующие запросы: \
                                {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"} \
                                {"dt_from": "2022-10-01T00:00:00", "dt_upto": "2022-11-30T23:59:00", "group_type": "day"} \
                                {"dt_from": "2022-02-01T00:00:00", "dt_upto": "2022-02-02T00:00:00", "group_type": "hour"}'\
                         )
    except Exception as ex:
        await msg.answer(text=f'Internal server error {ex}')


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
