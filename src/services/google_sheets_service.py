import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app_storage import AppStorage
from services.base_service import BaseService

logger = logging.getLogger(__name__)


class GoogleSheetsService(BaseService):
    def __init__(self):
        self.service = build("sheets", "v4", credentials=AppStorage().google_creds)

    def get_values(self, spreadsheet_id: str, range_name: str) -> list[list[str]]:
        try:
            result = (
                self.service.spreadsheets()
                .values()
                .batchGet(spreadsheetId=spreadsheet_id, ranges=range_name)
                .execute()
            )
            rows = result['valueRanges'][0]['values']

            logger.info(f"{len(rows)} rows retrieved from spreadsheet={spreadsheet_id} with range='{range_name}'.")

            return rows

        except HttpError as error:
            logger.exception(f"An error occurred: {error}")
