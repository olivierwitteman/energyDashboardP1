# DSMR v4.2 p1 using dsmr_parser and telegram objects

from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V5
from dsmr_parser.objects import CosemObject, MBusObject, Telegram
from dsmr_parser.parsers import TelegramParser
import os
import sys
import time


class energyMGMT:
    def __init__(self):
        self.erial_reader = SerialReader(
            device='/dev/ttyUSB0',
            serial_settings=SERIAL_SETTINGS_V5,
            telegram_specification=telegram_specifications.V4
        )

        # telegram = next(serial_reader.read_as_object())
        # print(telegram)
        self.verbose, self.logging = False, False
        self.powerhist = []
        self.lastlog = 0

    def log(self, msg):
        with open(f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.csv', 'a') as logfile:
            logfile.write(f'{time.time()},{log_msg}')
        self.lastlog = time.time()

try:
    arg = sys.argv[1]
    if arg == '-v':
        verbose = True
    elif arg == '-l':
        logging = True
except IndexError:
    arg = None

for telegram in serial_reader.read_as_object():

    if verbose:
        os.system('clear')
        print(telegram)
    else:
        powerhist.append(1000 * telegram.CURRENT_ELECTRICITY_USAGE.value)
        powerhist = powerhist[-min(5, len(powerhist)):]
        data = f'\rCurrent power usage: {round(sum(powerhist)/len(powerhist))} W'
        print(data, end='')

    if logging:
        log_msg = ''
        for attr, value in telegram:
            if 'LOG' not in attr:
                log_msg += f',{telegram.P1_MESSAGE_TIMESTAMP.value},{attr},{value.value}, {value.unit},\n'

        # time.sleep(5)
