from datetime import datetime
import logging
import sys

from dotenv import dotenv_values

from lib import Singleton

from services.google_auth_service import GoogleAuthService


class AppStorage(metaclass=Singleton):
    def __init__(self):
        self._google_creds = None
        self._google_auth_service = GoogleAuthService()
        self.env = type('EnvStorage', (), dotenv_values())
        self.__setup_logging()

    @property
    def google_creds(self):
        if self._google_creds is None:
            self._google_creds = self._google_auth_service.get_credentials(self.env.GOOGLE_AUTH_JSON_PATH)

        return self._google_creds

    @staticmethod
    def __setup_logging():
        log_filename = f'{datetime.now().strftime("%Y%m%d%H%M%S")}-sda-excellent-scheduler.log'
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s | %(message)s', '%H:%M:%S')
        handler = logging.FileHandler(f'logs/{log_filename}', mode='w')
        handler.setFormatter(formatter)
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.addHandler(screen_handler)
    
        return logger
