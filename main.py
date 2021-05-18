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

        self.general = 'P1_log.csv'
        self.minute = 'P1_log.minute'
        self.hour = 'P1_log.hour'
        self.day = 'P1_log.day'

        self.verbose, self.logging = False, False
        self.powerhist = []
        self.lastlog = {self.general: 0,
                        self.minute: 0,
                        self.hour: 0,
                        self.day: 0}

        try:
            arg = sys.argv[1]
            if arg == '-v':
                self.verbose = True
            elif arg == '-l':
                self.logging = True
        except IndexError:
            pass

    def log(self, msg, file='P1_log.csv'):
        """
        Appends message to log file
        :param msg:
        :param file:
        :return:
        """
        with open(f'{os.path.abspath(os.path.dirname(__file__))}/{file}', 'a') as logfile:
            logfile.write(f'{time.time()},{msg}')
        self.lastlog[file] = time.time()

    def write_register(self, payload: str):
        """
        Overwrites the current state file
        :param payload:
        :return:
        """
        with open(f'{os.path.abspath(os.path.dirname(__file__))}/P1.state', 'w') as register:
            register.write(str(payload))

    def trim_logs(self, lines_per_entry=21, minute_entries=1440, hour_entries=8760):
        os.system(
            f'echo "$(tail -{lines_per_entry * minute_entries} {os.path.abspath(os.path.dirname(__file__))}/{self.minute})" > {os.path.abspath(os.path.dirname(__file__))}/{self.minute}')

        os.system(
            f'echo "$(tail -{lines_per_entry * hour_entries} {os.path.abspath(os.path.dirname(__file__))}/{self.hour})" > {os.path.abspath(os.path.dirname(__file__))}/{self.hour}')

    def subscribe(self):
        for telegram in self.serial_reader.read_as_object():
            if self.verbose:
                os.system('clear')
                print(telegram)
            else:
                pass

            if self.logging:
                # Updates every cycle
                self.write_register(f'{telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value},'
                                    f'{telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value},'
                                    f'{telegram.CURRENT_ELECTRICITY_USAGE.value},'
                                    f'{telegram.CURRENT_ELECTRICITY_DELIVERY.value},'
                                    f'{telegram.ELECTRICITY_USED_TARIFF_1.value},'
                                    f'{telegram.ELECTRICITY_USED_TARIFF_2.value},'
                                    f'{telegram.ELECTRICITY_DELIVERED_TARIFF_1.value},'
                                    f'{telegram.ELECTRICITY_DELIVERED_TARIFF_2.value}')

                log_msg = ''
                for attr, value in telegram:
                    if 'LOG' not in attr:
                        log_msg += f',{telegram.P1_MESSAGE_TIMESTAMP.value},{attr},{value.value},{value.unit},\n'

                # Updates every minute
                if time.time() - self.lastlog[self.minute] >= 60:
                    self.log(msg=log_msg[1:], file=self.minute)

                # Updates every hour
                if time.time() - self.lastlog[self.hour] >= 60*60:
                    self.log(msg=log_msg[1:], file=self.hour)

                # Updates every day
                if time.time() - self.lastlog[self.day] >= 60*60*24:
                    self.log(msg=log_msg[1:], file=self.day)

                    # Trim log files once a day
                    self.trim_logs()


if __name__ == '__main__':
    while True:
        eMGMT = energyMGMT()
        try:
            eMGMT.subscribe()
        except Exception as e:
            eMGMT.log(e)