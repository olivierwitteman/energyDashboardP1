from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V4

from dsmr_parser.parsers import TelegramParser

serial_reader = SerialReader(
    device='/dev/ttyUSB0',
    serial_settings=SERIAL_SETTINGS_V4,
    telegram_specification=telegram_specifications.V4
)

parser = TelegramParser(telegram_specifications.V3)


# print(telegram)  # see 'Telegram object' docs below

for telegram in serial_reader.read():
    telegram = parser.parse(telegram)
    print(telegram)  # see 'Telegram object' docs below