# DSMR v4.2 p1 using dsmr_parser and telegram objects

from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V5
from dsmr_parser.objects import CosemObject, MBusObject, Telegram
from dsmr_parser.parsers import TelegramParser
import os
import sys

serial_reader = SerialReader(
    device='/dev/ttyUSB0',
    serial_settings=SERIAL_SETTINGS_V5,
    telegram_specification=telegram_specifications.V4
)

# telegram = next(serial_reader.read_as_object())
# print(telegram)

powerhist = []


print(sys.argv[1])


for telegram in serial_reader.read_as_object():
    # os.system('clear')

    powerhist.append(1000 * telegram.CURRENT_ELECTRICITY_USAGE.value)
    powerhist = powerhist[-min(5, len(powerhist)):]
    data = f'\rCurrent power usage: {round(sum(powerhist)/len(powerhist))} W'

    print(data, end='')