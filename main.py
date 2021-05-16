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
        self.serial_reader = SerialReader(
            device='/dev/ttyUSB0',
            serial_settings=SERIAL_SETTINGS_V5,
            telegram_specification=telegram_specifications.V4
        )


        self.verbose, self.logging = False, False
        self.powerhist = []
        self.lastlog = 0

        try:
            arg = sys.argv[1]
            if arg == '-v':
                self.verbose = True
            elif arg == '-l':
                self.logging = True
        except IndexError:
            pass

    def log(self, msg):
        with open(f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.csv', 'a') as logfile:
            logfile.write(f'{time.time()},{msg}')
        self.lastlog = time.time()

    def write_register(self, payload):
        print(payload)
        with open(f'{os.path.abspath(os.path.dirname(__file__))}/P1.state', 'w') as register:
            register.write(payload)

    def subscribe(self):
        for telegram in self.serial_reader.read_as_object():
            self.write_register(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value)

            if time.time() - self.lastlog >= 300:
                if self.verbose:
                    os.system('clear')
                    print(telegram)
                else:
                    pass

                if self.logging:
                    log_msg = ''
                    for attr, value in telegram:
                        if 'LOG' not in attr:
                            log_msg += f',{telegram.P1_MESSAGE_TIMESTAMP.value},{attr},{value.value},{value.unit},\n'
                    self.log(log_msg[1:])

            # time.sleep(58)


if __name__ == '__main__':
    while True:
        eMGMT = energyMGMT()
        try:
            eMGMT.subscribe()
        except Exception as e:
            eMGMT.log(e)