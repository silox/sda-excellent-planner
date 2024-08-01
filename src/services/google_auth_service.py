import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

from services.base_service import BaseService

logger = logging.getLogger(__name__)


class GoogleAuthService(BaseService):
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/calendar']

    @staticmethod
    def get_credentials(auth_file_path):
        logger.info('Attempting to authenticate Google API')

        creds = ServiceAccountCredentials.from_json_keyfile_name(auth_file_path, GoogleAuthService.scopes)
        if creds.invalid:
            logger.exception('Unable to authenticate (did you check the auth json file?)')
        else:
            logger.info('Authentication successfull')
        
        return creds
