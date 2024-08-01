from datetime import datetime

from lib.types import SheetRowGenerator
from lib.utils import norm_str
from services.google_sheets_service import GoogleSheetsService


class SDASheetFetcher:
    def __init__(self):
        self.google_sheets_service = GoogleSheetsService()

    def fetch_sheet_data(self, spreadsheet_id: str, range_name: str) -> list[list[str]]:
        return self.google_sheets_service.get_values(spreadsheet_id, range_name)

    @staticmethod
    def clean_filter_data_by_person(data: list[list[str]], name: str) -> SheetRowGenerator:
        for row in data[1:]:
            if len(row) != 7:
                continue

            date_str, _, time_interval_str, title, lesson_type, teacher_name, confirmed = row
            if norm_str(teacher_name) != norm_str(name) or norm_str(confirmed) != 'ano':
                continue

            start_time, end_time = SDASheetFetcher.convert_to_datetime_objects(date_str, time_interval_str)
            if end_time < datetime.now():
                continue

            yield start_time, end_time, f'{title} ({lesson_type})'
            
    @staticmethod
    def convert_to_datetime_objects(date_str: str, time_interval_str: str) -> tuple[datetime, datetime]:
        start_time_str, end_time_str = time_interval_str.replace(' ', '').split('-')
        
        start_time = datetime.strptime(f'{date_str} {start_time_str}', f'%d-%m-%Y %H:%M')
        end_time = datetime.strptime(f'{date_str} {end_time_str}', f'%d-%m-%Y %H:%M')
        return start_time, end_time
