from dotenv import load_dotenv

from app.sda_sheet_fetcher import SDASheetFetcher
from app_storage import AppStorage
from lib.types import SheetRowGenerator
from services.google_calendar_service import GoogleCalendarService

load_dotenv()


def fetch_sheets_data() -> SheetRowGenerator:
    sda_sheet_fetcher = SDASheetFetcher()
    data = sda_sheet_fetcher.fetch_sheet_data(AppStorage().env.GOOGLE_SHEET_ID, AppStorage().env.GOOGLE_SHEET_RANGE)
    yield from sda_sheet_fetcher.clean_filter_data_by_person(data, AppStorage().env.TEACHER_NAME)


def schedule_calendar_events(sheet_data_iter: SheetRowGenerator) -> None:
    google_calendar_service = GoogleCalendarService()
    existing_events = google_calendar_service.get_existing_events()

    for data in sheet_data_iter:
        if data in existing_events:
            continue

        google_calendar_service.insert_event(data)


def main() -> None:
    schedule_calendar_events(fetch_sheets_data())


if __name__ == "__main__":
    main()
