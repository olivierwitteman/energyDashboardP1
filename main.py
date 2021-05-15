from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V4

serial_reader = SerialReader(
    device='/dev/ttyUSB0',
    serial_settings=SERIAL_SETTINGS_V4,
    telegram_specification=telegram_specifications.V4
)

for telegram in serial_reader.read():
    print(telegram)  # see 'Telegram object' docs below