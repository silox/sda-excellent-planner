from datetime import datetime
import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytz

from app_storage import AppStorage
from services.base_service import BaseService

logger = logging.getLogger(__name__)


class GoogleCalendarService(BaseService):
    def __init__(self):
        self.service = build('calendar', 'v3', credentials=AppStorage().google_creds)

    def insert_event(self, data: tuple[datetime, datetime, str]) -> None:
        start_time, end_time, summary = data

        try:
            event = {
                'summary': summary,
                'description': 'Automatically generated event via SDA Excellent Planner.',
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Europe/Prague',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Europe/Prague',
                },
            }
            event_result = self.service.events().insert(calendarId='primary', body=event).execute()
            logger.info(f'Successfully created event: {event_result.get("htmlLink")}')

        except HttpError as error:
            logger.exception(f'An error occurred while inserting event to Google Calendars: {error}')


    def get_existing_events(self):
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=datetime.now(datetime.now().astimezone().tzinfo).isoformat(),
            singleEvents=True,
        ).execute()

        return self.__process_events(events_result.get('items', []))

    @staticmethod
    def __process_events(events: list[dict]) -> set[tuple[datetime, datetime, str]]:
        from_timezone = pytz.timezone("UTC")
        to_timezone= pytz.timezone("Europe/Prague")
        return {
            (
                GoogleCalendarService.__shift_timezone(event['start']['dateTime'], from_timezone, to_timezone),
                GoogleCalendarService.__shift_timezone(event['end']['dateTime'], from_timezone, to_timezone),
                event['summary'],
            ) for event in events
        }

    @staticmethod
    def __shift_timezone(date_str: str, from_timezone: pytz.timezone, to_timezone: pytz.timezone) -> datetime:
        naive_datetime = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        return from_timezone.localize(naive_datetime).astimezone(to_timezone).replace(tzinfo=None)
