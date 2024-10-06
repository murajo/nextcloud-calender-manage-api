import caldav
from textwrap import dedent
from datetime import datetime
from icalendar import Calendar

class NextCloudCalendarClient:
    def __init__(self, url, username, password, verify_ssl=False):
        try:
            self.client = caldav.DAVClient(url, username=username, password=password, ssl_verify_cert=verify_ssl)
            self.principal = self.client.principal()
        except Exception as e:
            print(f"Error initializing client: {e}")
            self.principal = None

    def get_calendar_by_name(self, calendar_name):
        try:
            calendars = self.principal.calendars()
            for calendar in calendars:
                if calendar.name == calendar_name:
                    return calendar
        except Exception as e:
            print(f"Error retrieving calendar: {e}")
        return None

    def get_calendars(self):
        try:
            return [calendar.name for calendar in self.principal.calendars()]
        except Exception as e:
            print(f"Error retrieving calendars: {e}")
            return False

    def format_datetime(self, dt):
        return dt.strftime('%Y%m%dT%H%M%SZ')

    def create_event_data(self, start_time, end_time, summary, description='', timezone='Asia/Tokyo'):
        uid = datetime.now().timestamp()
        created = self.format_datetime(datetime.now())
        dtstamp = self.format_datetime(datetime.now())
        dtstart = self.format_datetime(start_time)
        dtend = self.format_datetime(end_time)

        event_data = dedent(f"""
        BEGIN:VCALENDAR
        BEGIN:VEVENT
        VERSION:2.0
        UID:{uid}
        CREATED:{created}
        DTSTAMP:{dtstamp}
        DTSTART;TZID={timezone}:{dtstart}
        DTEND;TZID={timezone}:{dtend}
        SUMMARY:{summary}
        TZID:{timezone}
        DESCRIPTION:{description}
        END:VEVENT
        END:VCALENDAR
        """).strip()

        return event_data

    def add_event(self, calendar_name, start_time, end_time, summary, description, timezone):
        try:
            calendar = self.get_calendar_by_name(calendar_name)
            if calendar:
                event_data = self.create_event_data(start_time, end_time, summary, description, timezone)
                calendar.add_event(event_data)
                return f"Event added to {calendar_name}"
            return "Calendar not found"
        except Exception as e:
            print(f"Error adding event: {e}")
            return False

    def delete_event(self, calendar_name, event_summary):
        try:
            calendar = self.get_calendar_by_name(calendar_name)
            if not calendar:
                return "Calendar not found"
            
            events = calendar.events()
            for event in events:
                if event_summary in event.data:
                    event.delete()
                    return f"Event '{event_summary}' deleted from {calendar_name}"
            return "Event not found"
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False

    def get_events(self, calendar_name):
        try:
            calendar = self.get_calendar_by_name(calendar_name)
            if not calendar:
                return "Calendar not found"
            
            event_list = []
            for event in calendar.events():
                event_list.append(Calendar.from_ical(event.data))
            return event_list
        except Exception as e:
            print(f"Error retrieving events: {e}")
            return False

    def event_exists(self, calendar_name, summary):
        try:
            events = self.get_events(calendar_name)
            if events is False:
                return False
            return any(event.walk('VEVENT')[0]['SUMMARY'] == summary for event in events)
        except Exception as e:
            print(f"Error checking if event exists: {e}")
            return False